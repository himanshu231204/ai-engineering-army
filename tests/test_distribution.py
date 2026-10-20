"""Offline distribution regression checks; no Claude installation required."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

from tools import aiea


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)

    def run_cli(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(aiea.ROOT / "tools/aiea.py"), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def package(self, host, *args, output=None):
        destination = output or self.output
        self.run_cli("package", "--host", host, "--output", str(destination), *args)
        version = aiea.VERSION_FILE.read_text().strip()
        return destination / f"aiea-{version}-{host}.zip"

    def test_validation_and_groups(self):
        self.run_cli("validate")
        for group, count in (("core", 10), ("specialists", 7)):
            self.assertTrue(self.run_cli("list", "--group", group).stdout.strip().endswith(f"{count} skills"))

    def test_expanded_inventory_and_discovery_cover_the_same_skills(self):
        skills, errors = aiea.load_skills()
        self.assertEqual(errors, [])
        self.assertEqual(len(skills), 17)
        added = {"repository-reconnaissance", "requirements-discovery", "architecture-design",
                 "task-planning", "implementation-workflow", "integration-handoff",
                 "testing-review", "browser-qa-review"}
        self.assertTrue(added <= {skill.name for skill in skills})
        reference = (aiea.SKILLS_ROOT / "aiea-bootstrap/references/discovery.md").read_text()
        routed = {line.split("|")[1].strip() for line in reference.splitlines()
                  if line.startswith("| ") and not line.startswith("| Skill name")}
        self.assertEqual(routed, {skill.name for skill in skills})

    def test_codex_plugin_package_is_a_self_contained_local_marketplace(self):
        with zipfile.ZipFile(self.package("codex-plugin")) as archive:
            plugin = json.loads(archive.read(".codex-plugin/plugin.json"))
            self.assertEqual(plugin["name"], aiea.PLUGIN_NAME)
            self.assertEqual(plugin["skills"], "./skills/")
            market = json.loads(archive.read(".agents/plugins/marketplace.json"))
            self.assertEqual(market["name"], "aiea-marketplace")
            entry, = market["plugins"]
            self.assertEqual(entry["source"], {"source": "local", "path": "./"})
            self.assertEqual(entry["name"], plugin["name"])
            self.assertNotIn("hooks", plugin)

    def test_opencode_plugin_runs_offline_and_registers_packaged_skills(self):
        if not shutil.which("node"):
            self.skipTest("Node.js is required for the OpenCode adapter contract test")
        directory = self.output / "opencode-plugin"
        with zipfile.ZipFile(self.package("opencode-plugin")) as archive:
            archive.extractall(directory)
        result = subprocess.run(
            ["node", "--test", str(aiea.ROOT / "tests/opencode-plugin.test.mjs")],
            env=os.environ | {"AIEA_TEST_PLUGIN": str(directory)},
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_new_plugin_subsets_only_reference_included_skills(self):
        for host in ("codex-plugin", "opencode-plugin"):
            with self.subTest(host=host), zipfile.ZipFile(self.package(
                    host, "--skill", "aiea-bootstrap")) as archive:
                self.assertEqual([n for n in archive.namelist() if n.endswith('/SKILL.md')],
                                 ["skills/aiea-bootstrap/SKILL.md"])
                if host == "opencode-plugin":
                    self.assertEqual([s["name"] for s in json.loads(archive.read("skills-index.json"))],
                                     ["aiea-bootstrap"])

    def test_canonical_skills_match_direct_host_discovery(self):
        skills, errors = aiea.load_skills()
        self.assertEqual(errors, [])
        discoverable = {p.parent.name for p in aiea.SKILLS_ROOT.glob("*/SKILL.md")}
        self.assertEqual(discoverable, {skill.name for skill in skills})

    def registry_fixture(self):
        root = self.output / "registry-fixture"
        for name in ("custom-workflow", "custom-review"):
            path = root / ".agents/skills" / name / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(f"---\nname: {name}\ndescription: Review the supplied task.\n---\n", encoding="utf-8")
        registry = {"skills": [
            {"name": "custom-workflow", "group": "core"},
            {"name": "custom-review", "group": "specialists"},
        ]}
        (root / "skill-registry.json").write_text(json.dumps(registry), encoding="utf-8")
        return root, registry

    def test_registry_controls_groups_without_directory_nesting(self):
        root, _ = self.registry_fixture()
        skills, errors = aiea.load_skills(root)
        self.assertEqual(errors, [])
        self.assertEqual({skill.name: skill.group for skill in skills},
                         {"custom-workflow": "core", "custom-review": "specialists"})

    def test_registry_rejects_incomplete_or_invalid_membership(self):
        root, registry = self.registry_fixture()
        entries = registry["skills"]
        cases = [entries[:1], entries + entries[:1],
                 entries + [{"name": "absent", "group": "core"}],
                 [{"name": "custom-workflow", "group": "other"}, entries[1]],
                 [None], "invalid"]
        for value in cases:
            with self.subTest(value=value):
                (root / "skill-registry.json").write_text(json.dumps({"skills": value}), encoding="utf-8")
                _, errors = aiea.load_skills(root)
                self.assertTrue(errors)

    def test_nested_skills_are_rejected_instead_of_silently_packaged(self):
        root, _ = self.registry_fixture()
        source = root / ".agents/skills/custom-review"
        destination = root / ".agents/skills/specialists/custom-review"
        destination.parent.mkdir()
        shutil.move(str(source), str(destination))
        _, errors = aiea.load_skills(root)
        self.assertTrue(any("direct" in error for error in errors), errors)

    def test_all_package_layouts_and_hashes(self):
        skills, errors = aiea.load_skills()
        self.assertEqual(errors, [])
        for host, prefix in aiea.HOST_PATHS.items():
            with self.subTest(host=host), zipfile.ZipFile(self.package(host)) as archive:
                self.assertIsNone(archive.testzip())
                self.assertTrue(all(info.create_system == 3 for info in archive.infolist()),
                                "ZIP creator platform must be fixed for cross-platform reproducibility")
                license_name = "LICENSE" if host in aiea.PLUGIN_HOSTS else "AIEA-LICENSE.txt"
                self.assertEqual(archive.read(license_name), (aiea.ROOT / "LICENSE").read_bytes())
                manifest = json.loads(archive.read("aiea-manifest.json"))
                self.assertEqual(set(manifest["skills"]), {skill.name for skill in skills})
                self.assertEqual(set(archive.namelist()), {f["path"] for f in manifest["files"]} | {"aiea-manifest.json"})
                for item in manifest["files"]:
                    content = archive.read(item["path"])
                    self.assertEqual(len(content), item["size"])
                    self.assertEqual(hashlib.sha256(content).hexdigest(), item["sha256"])
                for skill in skills:
                    self.assertEqual(archive.read(f"{prefix}/{skill.name}/SKILL.md"), (skill.path / "SKILL.md").read_bytes())
                if host == "claude-code-plugin":
                    plugin = json.loads(archive.read(".claude-plugin/plugin.json"))
                    self.assertEqual(plugin["name"], aiea.PLUGIN_NAME)
                    self.assertEqual(plugin["version"], manifest["version"])
                    self.assertNotIn("skills", plugin)  # No checkout-relative paths.
                    self.assertIn("LICENSE", archive.namelist())
                    self.assertNotIn(".claude-plugin/marketplace.json", archive.namelist())
                else:
                    self.assertNotIn(".claude-plugin/plugin.json", archive.namelist())
                    if host not in aiea.PLUGIN_HOSTS:
                        self.assertNotIn("LICENSE", archive.namelist())  # Preserve the target project's license.

    def test_adapter_metadata_rejects_version_and_layout_drift(self):
        root = self.output / "adapter-fixture"
        for relative in (".codex-plugin/plugin.json", "adapters/opencode/plugin/package.json",
                         "adapters/opencode/plugin/index.js"):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(aiea.ROOT / relative, destination)
        version = aiea.VERSION_FILE.read_text().strip()
        self.assertEqual(aiea.adapter_errors(root, version), [])
        for relative in (".codex-plugin/plugin.json", "adapters/opencode/plugin/package.json"):
            path = root / relative
            original = path.read_bytes()
            document = json.loads(original)
            for broken in (document | {"version": "0.0.0"}, None, []):
                path.write_text(json.dumps(broken))
                self.assertTrue(aiea.adapter_errors(root, version))
            path.write_bytes(original)

    def test_subset_and_reproducibility(self):
        args = ("--skill", "security-review", "--skill", "aiea-bootstrap", "--skill", "security-review")
        first = self.package("claude-code-plugin", *args)
        second = self.package("claude-code-plugin", *args, output=self.output / "repeat")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(json.loads(archive.read("aiea-manifest.json"))["skills"], ["aiea-bootstrap", "security-review"])
            self.assertEqual(len([n for n in archive.namelist() if n.endswith("/SKILL.md")]), 2)

    def test_bootstrap_only_packages_keep_the_discovery_reference(self):
        reference = "aiea-bootstrap/references/discovery.md"
        expected = (aiea.SKILLS_ROOT / reference).read_bytes()
        for host, prefix in aiea.HOST_PATHS.items():
            with self.subTest(host=host), zipfile.ZipFile(
                    self.package(host, "--skill", "aiea-bootstrap")) as archive:
                self.assertEqual(archive.read(f"{prefix}/{reference}"), expected)
                self.assertEqual(json.loads(archive.read("aiea-manifest.json"))["skills"],
                                 ["aiea-bootstrap"])

    def test_refuses_overwrite_and_unknown_skill(self):
        archive = self.package("claude-code-plugin")
        before = archive.read_bytes()
        self.run_cli("package", "--host", "claude-code-plugin", "--output", str(self.output), code=2)
        self.assertEqual(archive.read_bytes(), before)
        self.run_cli("package", "--host", "claude-code-plugin", "--skill", "missing-skill", "--output", str(self.output / "unknown"), code=2)
        self.assertFalse((self.output / "unknown").exists())

    def test_release_bundle_checksums_and_overwrite_protection(self):
        destination = self.output / "release"
        self.run_cli("release", "--output", str(destination))
        version = aiea.VERSION_FILE.read_text().strip()
        expected = {f"aiea-{version}-{host}.zip" for host in aiea.HOST_PATHS}
        expected.add("RELEASE-NOTES.md")
        self.assertEqual({p.name for p in destination.iterdir()}, expected | {"SHA256SUMS"})
        checksums = {}
        for line in (destination / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ", 1)
            checksums[name] = digest
        self.assertEqual(set(checksums), expected)
        for name, digest in checksums.items():
            self.assertEqual(hashlib.sha256((destination / name).read_bytes()).hexdigest(), digest)
        before = {p.name: p.read_bytes() for p in destination.iterdir()}
        self.run_cli("release", "--output", str(destination), code=2)
        self.assertEqual({p.name: p.read_bytes() for p in destination.iterdir()}, before)
        repeat = self.output / "repeat-release"
        self.run_cli("release", "--output", str(repeat))
        self.assertEqual({p.name: p.read_bytes() for p in repeat.iterdir()}, before)
        empty = self.output / "existing-empty"
        empty.mkdir()
        self.run_cli("release", "--output", str(empty), code=2)
        self.assertEqual(list(empty.iterdir()), [])

    def test_plugin_manifest_carries_listing_metadata(self):
        plugin = json.loads((aiea.ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertTrue(plugin.get("displayName"), "the directory listing needs a displayName")
        self.assertTrue(plugin.get("description"))
        self.assertTrue(plugin.get("documentationUrl"), "the directory listing needs a documentation link")
        self.assertTrue(plugin.get("supportUrl"), "the directory listing needs a support link")

    def test_marketplace_migrates_the_previous_plugin_name(self):
        marketplace = json.loads(
            (aiea.ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        renames = marketplace.get("renames")
        self.assertIsInstance(renames, dict)
        self.assertIn("aiea", renames)
        self.assertEqual(renames["aiea"], aiea.PLUGIN_NAME)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], aiea.PLUGIN_NAME)

    def test_rejects_manifest_drift(self):
        root = self.output / "repo"
        shutil.copytree(aiea.ROOT / ".claude-plugin", root / ".claude-plugin")
        shutil.copytree(aiea.SKILLS_ROOT, root / ".agents/skills")
        shutil.copy2(aiea.ROOT / "skill-registry.json", root / "skill-registry.json")
        skills, _ = aiea.load_skills(root)
        version = aiea.VERSION_FILE.read_text().strip()
        self.assertEqual(aiea.plugin_errors(root, skills, version), [])
        path = root / ".claude-plugin/plugin.json"
        original = json.loads(path.read_text())
        for change in ({"version": "0.0.0"}, {"skills": original["skills"][:-1]},
                       {"skills": ["./../outside"]}, {"skills": original["skills"] * 2},
                       {"skills": None}, {"name": "other"}):
            with self.subTest(change=change):
                path.write_text(json.dumps(original | change))
                self.assertTrue(aiea.plugin_errors(root, skills, version))
        path.write_text(json.dumps(original))
        marketplace = root / ".claude-plugin/marketplace.json"
        original_market = json.loads(marketplace.read_text())
        for plugins in ([], [{"name": aiea.PLUGIN_NAME, "source": "./missing"}], None):
            marketplace.write_text(json.dumps(original_market | {"plugins": plugins}))
            self.assertTrue(aiea.plugin_errors(root, skills, version))
        marketplace.write_text(json.dumps(original_market))
        for invalid in ("{", "[]", "null"):
            path.write_text(invalid)
            self.assertTrue(aiea.plugin_errors(root, skills, version))


if __name__ == "__main__":
    unittest.main()

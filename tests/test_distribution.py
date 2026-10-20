"""Offline distribution regression checks; no Claude installation required."""

import hashlib
import json
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
        for group, count in (("core", 4), ("specialists", 5)):
            self.assertTrue(self.run_cli("list", "--group", group).stdout.strip().endswith(f"{count} skills"))

    def test_all_package_layouts_and_hashes(self):
        skills, errors = aiea.load_skills()
        self.assertEqual(errors, [])
        for host, prefix in aiea.HOST_PATHS.items():
            with self.subTest(host=host), zipfile.ZipFile(self.package(host)) as archive:
                self.assertIsNone(archive.testzip())
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
                    self.assertEqual(plugin["name"], "aiea")
                    self.assertEqual(plugin["version"], manifest["version"])
                    self.assertNotIn("skills", plugin)  # No checkout-relative paths.
                    self.assertIn("LICENSE", archive.namelist())
                    self.assertNotIn(".claude-plugin/marketplace.json", archive.namelist())
                else:
                    self.assertNotIn(".claude-plugin/plugin.json", archive.namelist())

    def test_subset_and_reproducibility(self):
        args = ("--skill", "security-review", "--skill", "aiea-bootstrap", "--skill", "security-review")
        first = self.package("claude-code-plugin", *args)
        second = self.package("claude-code-plugin", *args, output=self.output / "repeat")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(json.loads(archive.read("aiea-manifest.json"))["skills"], ["aiea-bootstrap", "security-review"])
            self.assertEqual(len([n for n in archive.namelist() if n.endswith("/SKILL.md")]), 2)

    def test_refuses_overwrite_and_unknown_skill(self):
        archive = self.package("claude-code-plugin")
        before = archive.read_bytes()
        self.run_cli("package", "--host", "claude-code-plugin", "--output", str(self.output), code=2)
        self.assertEqual(archive.read_bytes(), before)
        self.run_cli("package", "--host", "claude-code-plugin", "--skill", "missing-skill", "--output", str(self.output / "unknown"), code=2)
        self.assertFalse((self.output / "unknown").exists())

    def test_rejects_manifest_drift(self):
        root = self.output / "repo"
        shutil.copytree(aiea.ROOT / ".claude-plugin", root / ".claude-plugin")
        shutil.copytree(aiea.SKILLS_ROOT, root / ".agents/skills")
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
        for plugins in ([], [{"name": "aiea", "source": "./missing"}], None):
            marketplace.write_text(json.dumps(original_market | {"plugins": plugins}))
            self.assertTrue(aiea.plugin_errors(root, skills, version))
        marketplace.write_text(json.dumps(original_market))
        for invalid in ("{", "[]", "null"):
            path.write_text(invalid)
            self.assertTrue(aiea.plugin_errors(root, skills, version))


if __name__ == "__main__":
    unittest.main()

"""Offline checks for the declarative version registry in `.version-bump.json`."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from tools import aiea


class VersionRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)

    def make_fixture(self, version="1.2.3", extra=None):
        """Build a small repository with a text version file and a JSON manifest."""
        root = self.output / "fixture"
        (root / "manifests").mkdir(parents=True)
        (root / "VERSION").write_text(f"{version}\n", encoding="utf-8")
        (root / "manifests" / "plugin.json").write_text(
            json.dumps({"name": "aiea", "version": version, "description": "x"}, indent=2) + "\n",
            encoding="utf-8",
        )
        (root / ".version-bump.json").write_text(json.dumps({
            "files": [
                {"path": "VERSION", "field": "text"},
                {"path": "manifests/plugin.json", "field": "version"},
            ],
            "audit": {"exclude": ["*.md"]},
        }, indent=2) + "\n", encoding="utf-8")
        if extra is not None:
            (root / "notes.md").write_text(extra, encoding="utf-8")
        return root

    def test_check_reports_declared_versions_and_no_drift(self):
        root = self.make_fixture()
        rows, errors = aiea.declared_versions(root)
        self.assertEqual(errors, [])
        self.assertEqual({entry.path for entry, _ in rows}, {"VERSION", "manifests/plugin.json"})
        self.assertEqual({value for _, value in rows}, {"1.2.3"})
        self.assertEqual(aiea.version_errors(root), [])
        self.assertEqual(aiea.run_version(root), 0)

    def test_drift_between_declared_files_is_reported(self):
        root = self.make_fixture()
        (root / "manifests" / "plugin.json").write_text(
            json.dumps({"name": "aiea", "version": "1.2.4"}, indent=2) + "\n", encoding="utf-8")
        errors = aiea.version_errors(root)
        self.assertTrue(errors)
        self.assertIn("not in sync", errors[0])
        self.assertEqual(aiea.run_version(root), 1)

    def test_bump_updates_every_declared_file(self):
        root = self.make_fixture()
        self.assertEqual(aiea.run_version(root, new_version="2.0.0"), 0)
        self.assertEqual((root / "VERSION").read_text(encoding="utf-8"), "2.0.0\n")
        manifest = json.loads((root / "manifests" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "2.0.0")
        self.assertEqual(aiea.version_errors(root), [])

    def test_bump_keeps_the_rest_of_each_manifest_unchanged(self):
        root = self.make_fixture()
        before = (root / "manifests" / "plugin.json").read_text(encoding="utf-8")
        aiea.run_version(root, new_version="2.0.0")
        after = (root / "manifests" / "plugin.json").read_text(encoding="utf-8")
        self.assertEqual(before.replace("1.2.3", "2.0.0"), after)

    def test_bump_is_atomic_when_a_declared_file_is_unreadable(self):
        root = self.make_fixture()
        broken = root / "manifests" / "plugin.json"
        broken.write_text("{not json", encoding="utf-8")
        before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
        self.assertEqual(aiea.run_version(root, new_version="2.0.0"), 1)
        after = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_audit_reports_undeclared_version_references(self):
        root = self.make_fixture(extra="documents version 1.2.3 in prose\n")
        findings = aiea.audit_versions(root)
        self.assertEqual(findings, [])
        (root / "tool.py").write_text("VERSION = \"1.2.3\"\n", encoding="utf-8")
        findings = aiea.audit_versions(root)
        self.assertEqual(findings, ["tool.py"])
        self.assertEqual(aiea.run_version(root, audit=True), 1)

    def test_audit_does_not_match_a_longer_version_number(self):
        root = self.make_fixture()
        (root / "tool.py").write_text("other = \"1.2.30\"\n", encoding="utf-8")
        self.assertEqual(aiea.audit_versions(root), [])

    def test_bump_rejects_a_malformed_version(self):
        root = self.make_fixture()
        before = (root / "VERSION").read_bytes()
        self.assertEqual(aiea.run_version(root, new_version="not-a-version"), 2)
        self.assertEqual((root / "VERSION").read_bytes(), before)

    def test_missing_declared_file_is_reported_without_writes(self):
        root = self.make_fixture()
        (root / "manifests" / "plugin.json").unlink()
        errors = aiea.version_errors(root)
        self.assertTrue(errors)
        self.assertEqual(aiea.run_version(root, new_version="2.0.0"), 1)
        self.assertEqual((root / "VERSION").read_text(encoding="utf-8"), "1.2.3\n")

    def test_real_registry_covers_every_version_bearing_manifest(self):
        entries, excludes, mentions, errors = aiea.bump_registry(aiea.ROOT)
        self.assertEqual(errors, [])
        self.assertTrue(entries)
        self.assertTrue(excludes)
        self.assertTrue(mentions)
        declared = {entry.path for entry in entries}
        for required in ("VERSION", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
                         "adapters/opencode/plugin/package.json"):
            self.assertIn(required, declared)
        rows, read_errors = aiea.declared_versions(aiea.ROOT)
        self.assertEqual(read_errors, [])
        self.assertEqual({value for _, value in rows}, {aiea.VERSION_FILE.read_text().strip()})

    def test_real_registry_matches_the_release_workflow_expectations(self):
        entries, _, _, _ = aiea.bump_registry(aiea.ROOT)
        fields = {(entry.path, entry.field) for entry in entries}
        self.assertIn(("VERSION", "text"), fields)
        self.assertIn((".claude-plugin/plugin.json", "version"), fields)

    def test_bump_preserves_the_formatting_of_a_real_manifest(self):
        root = self.output / "real"
        root.mkdir()
        shutil.copy2(aiea.ROOT / ".codex-plugin/plugin.json", root / "plugin.json")
        (root / ".version-bump.json").write_text(json.dumps({
            "files": [{"path": "plugin.json", "field": "version"}],
            "audit": {"exclude": []},
        }), encoding="utf-8")
        before = (root / "plugin.json").read_text(encoding="utf-8")
        current = aiea.VERSION_FILE.read_text(encoding="utf-8-sig").strip()
        aiea.run_version(root, new_version="9.9.9")
        after = (root / "plugin.json").read_text(encoding="utf-8")
        # Only the version value changes; the rest of the manifest keeps its
        # exact original formatting.
        self.assertEqual(before.replace(f'"{current}"', '"9.9.9"'), after)

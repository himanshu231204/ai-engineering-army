"""Offline checks for the GitHub issue and pull request templates."""

import json
from pathlib import Path
import re
import unittest

from tools import aiea

TEMPLATE_ROOT = aiea.ROOT / ".github" / "ISSUE_TEMPLATE"
PR_TEMPLATE = aiea.ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"


def frontmatter(text):
    """Return the YAML-ish frontmatter of a Markdown template as a dict."""
    if not text.startswith("---\n"):
        return {}
    block = text.split("---", 2)[1]
    fields = {}
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


class TemplateTests(unittest.TestCase):
    def test_every_issue_template_declares_name_about_and_labels(self):
        templates = sorted(TEMPLATE_ROOT.glob("*.md"))
        self.assertTrue(templates)
        for template in templates:
            with self.subTest(template=template.name):
                fields = frontmatter(template.read_text(encoding="utf-8"))
                self.assertTrue(fields.get("name"), "a template needs a name")
                self.assertTrue(fields.get("about"), "a template needs an about line")
                labels = fields.get("labels", "")
                self.assertTrue(labels, "a template needs at least one label")
                for label in (part.strip() for part in labels.split(",")):
                    self.assertRegex(label, r"^[a-z0-9][a-z0-9-]*$")

    def test_template_labels_exist_in_the_repository(self):
        known = {
            "accessibility", "bug", "documentation", "duplicate", "enhancement",
            "evidence-report", "good first issue", "help wanted", "invalid",
            "new-host", "question", "wontfix",
        }
        for template in sorted(TEMPLATE_ROOT.glob("*.md")):
            fields = frontmatter(template.read_text(encoding="utf-8"))
            for label in (part.strip() for part in fields.get("labels", "").split(",")):
                with self.subTest(template=template.name, label=label):
                    self.assertIn(label, known)

    def test_blank_issues_are_disabled_and_questions_have_a_destination(self):
        config = (TEMPLATE_ROOT / "config.yml").read_text(encoding="utf-8")
        self.assertIn("blank_issues_enabled: false", config)
        self.assertIn("contact_links:", config)
        self.assertIn("discussions", config)

    def test_pull_request_template_requires_evidence_and_human_review(self):
        text = PR_TEMPLATE.read_text(encoding="utf-8")
        for heading in ("Who is submitting this PR?", "What problem are you trying to solve?",
                        "What does this PR change?", "Is this change appropriate for core AIEA?",
                        "What alternatives did you consider?",
                        "Does this PR contain multiple unrelated changes?",
                        "Environment tested", "Evidence and verification", "Human review"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        self.assertIn("- [ ] A human has reviewed the COMPLETE proposed diff before submission", text)

    def test_pull_request_template_names_the_repository_checks(self):
        text = PR_TEMPLATE.read_text(encoding="utf-8")
        for command in ("python tools/aiea.py validate",
                        "python -m unittest discover -s tests -v",
                        "python tools/aiea.py version --audit"):
            with self.subTest(command=command):
                self.assertIn(command, text)

    def test_templates_are_required_repository_documents(self):
        required = set(aiea.REQUIRED_DOCS)
        for relative in (".github/PULL_REQUEST_TEMPLATE.md",
                         ".github/ISSUE_TEMPLATE/config.yml",
                         ".github/ISSUE_TEMPLATE/bug_report.md",
                         ".github/ISSUE_TEMPLATE/evidence_report.md",
                         ".github/ISSUE_TEMPLATE/feature_request.md",
                         ".github/ISSUE_TEMPLATE/new_host.md"):
            with self.subTest(relative=relative):
                self.assertIn(relative, required)

    def test_new_host_template_matches_the_supported_host_vocabulary(self):
        text = (TEMPLATE_ROOT / "new_host.md").read_text(encoding="utf-8")
        for host in ("Claude Code", "Codex", "OpenCode"):
            with self.subTest(host=host):
                self.assertIn(host, text)

    def test_issue_templates_do_not_leak_machine_specific_paths(self):
        for template in sorted(TEMPLATE_ROOT.glob("*.md")):
            text = template.read_text(encoding="utf-8")
            with self.subTest(template=template.name):
                self.assertNotRegex(text, r"[A-Za-z]:\\\\?Users\\\\?")
                self.assertNotIn("/home/", text)

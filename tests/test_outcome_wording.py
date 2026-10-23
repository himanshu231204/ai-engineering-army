"""The scoped-outcome wording must stay identical wherever a skill defines outcomes."""

from pathlib import Path
import shutil
import tempfile
import unittest

from tools import aiea


class OutcomeWordingTests(unittest.TestCase):
    def test_repository_skills_carry_the_static_evidence_rule(self):
        self.assertEqual(aiea.outcome_errors(), [])

    def test_a_skill_missing_the_rule_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(aiea.SKILLS_ROOT, root / ".agents/skills")
            target = root / ".agents/skills/security-review/SKILL.md"
            text = target.read_text(encoding="utf-8")
            self.assertIn(aiea.STATIC_EVIDENCE_RULE, " ".join(text.split()))
            target.write_text(" ".join(text.split()).replace(aiea.STATIC_EVIDENCE_RULE, ""), encoding="utf-8")
            errors = aiea.outcome_errors(root)
            self.assertTrue(any("security-review" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()

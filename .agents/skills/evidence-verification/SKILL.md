---
name: evidence-verification
description: Use before declaring software work complete to choose relevant checks, inspect their results, and make completion claims that match available evidence.
license: MIT
---

# Evidence-based verification

1. Identify the behavior changed and the smallest relevant checks for it.
2. Run checks appropriate to the user's request and repository guidance. Do not substitute a check that cannot exercise the changed behavior.
3. Inspect exit status and useful output. For browser or live integrations, inspect the actual resulting behavior when that level was requested.
4. Record each check as passed, failed, or not run. Explain why a required check could not run.
5. Review the final diff for unrelated changes and obvious regressions.
6. State what the evidence establishes and what remains unverified. Do not claim broad correctness from narrow checks.

A specialist report, a proposed test, or a successful build alone does not prove runtime behavior unless that is what the claim concerns.

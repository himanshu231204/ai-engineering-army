---
name: bounded-repair
description: Use when a relevant implementation or validation check fails, to diagnose from evidence and repair within an explicit attempt limit without masking unresolved failures.
license: MIT
---

# Bounded repair

1. Capture the failing command, output, and affected behavior.
2. Find the smallest plausible cause using current code and direct evidence. Do not hide the failure by weakening or deleting the check.
3. Set a small repair budget appropriate to the task and tell the lead what remains after each attempt.
4. Make one coherent repair at a time, then rerun the failing check and any nearby regression checks.
5. If the issue persists or evidence is insufficient, stop at the budget, report the blocker, and distinguish verified behavior from assumptions.
6. Do not broaden scope silently to unrelated refactors.

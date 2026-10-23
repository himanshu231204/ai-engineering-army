---
name: bounded-repair
description: Use when a relevant implementation or validation check fails, to diagnose from evidence and repair within an explicit attempt limit without masking unresolved failures.
license: MIT
---

# Bounded repair

1. Capture the failing command, output, affected behavior, and stable failure
   ID in the active run ledger. Recover its counters before proceeding.
   If the bootstrap ledger template is not installed, keep an equivalent record
   in session with run/scope/revision, failure IDs, limits, reserved attempts,
   evidence, blockers, outcome, and next action. Persist it only when authorized;
   never record secrets or personal data.
2. Find the smallest plausible cause using current code and direct evidence. Do not hide the failure by weakening or deleting the check.
3. Unless the user explicitly overrides them, cap repairs at two attempts per
   failure ID and five per run. Carry counts through delegation, skill reloads,
   handoffs, and resumed sessions. Never silently reset or increase a limit. If
   prior counters are unrecoverable, stop without repairing and report a
   blocker.
4. Reserve/count an attempt in the ledger before any corrective change; an
   interrupted, reverted, or unverified attempt counts. Diagnosis and
   unchanged-artifact rechecks do not consume attempts. A repair for multiple
   failures counts against every affected failure and once against the run.
5. Make one coherent repair at a time, then rerun the failing check and nearby
   regressions without changing independent requirements or test expectations.
   Stop when either limit is reached.
6. Report exactly one scoped outcome: Failed (a required check confirms a
   remaining defect), Blocked (an external prerequisite prevents completion and
   no confirmed failure takes precedence), Inconclusive (evidence is
   insufficient, stale, flaky, or conflicting), or Verified (all scoped required
   checks pass at final state). Include revision, evidence, counts/limits,
   limitations, and next action. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown. Do not imply runtime verification from static
   evidence.

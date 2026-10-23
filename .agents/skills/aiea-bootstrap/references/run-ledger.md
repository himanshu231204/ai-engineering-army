# AIEA run ledger

Use this compact record to preserve task scope, evidence, and repair accounting
across delegation, skill reloads, handoffs, and resumed sessions. Keep it in the
active session by default. Write it to a file only when the user has authorized
that file and location. Never include secrets, credentials, tokens, or personal
data. Record only information needed to identify the work and its evidence.

Copy this template into the session and update it as work proceeds:

```text
Run ID:
Goal and scope:
AIEA revision (commit or source identity):
Target revision (commit or source identity):
Working-tree state (clean/dirty; relevant paths, no private contents):
Host and version:
Activation evidence (native inventory, explicit load, automatic selection, or unavailable):
Actual loaded skills (names and evidence; do not infer):
Acceptance checks (required check IDs, commands/observations, expected result):
Specialist assignments (skill, bounded question, read-only scope, status, evidence):

Repair accounting:
  Explicit user override (if any):
  Per-failure limit (default 2):
  Run-wide limit (default 5):
  Stable failure IDs and observed baseline evidence:
  Reserved attempts (failure ID(s), run attempt number, reservation time/order, change, result):
  Remaining attempts per failure and run:
  If counters cannot be recovered, record the uncertainty and stop repairs.

Evidence (check ID, command/observation, revision, result, timestamp/source):
Blockers (external prerequisite and affected checks):
Scoped outcome (choose exactly one: Failed / Blocked / Inconclusive / Verified):
Limitations (including unrun behavior):
Next action:
```

## Repair accounting rules

- Unless the user explicitly sets another limit, allow at most two corrective
  attempts for each stable failure ID and five corrective attempts total in the
  run. Record an override verbatim and do not increase it later without a new
  explicit user instruction.
- Reserve and count an attempt in this ledger before changing code or other
  artifacts to correct a failure. Interrupted, reverted, or unverified changes
  still count. Diagnosis and checks that leave the artifact unchanged do not.
- A single repair that addresses several failure IDs counts once against each
  affected failure and once against the run-wide total.
- Carry failure IDs, limits, reservations, and counts across specialists,
  loaded-skill changes, handoffs, and resumed sessions. Never silently reset
  counters. If earlier counts cannot be recovered, make no further repairs and
  report the accounting blocker.
- Stop repairs when either applicable limit is reached. Preserve unrelated
  requirements and test expectations when reporting the remaining result.

## Scoped terminal outcomes

Choose exactly one outcome for the stated scope:

- **Failed** — a required check confirms a remaining defect.
- **Blocked** — no confirmed failure takes precedence, but an external
  prerequisite prevents completion.
- **Inconclusive** — evidence is insufficient, stale, flaky, or conflicting.
- **Verified** — all required scoped acceptance checks pass at the final state.

A static review can be Verified as a static review; it cannot establish runtime
behavior. Report outcome, scope/revision, changes or findings, actual evidence,
repair counts and limits, limitations, and next action. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown.

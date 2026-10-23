---
name: frontend-review
description: Use for read-only analysis of frontend behavior, accessibility, state, API contracts, and user-visible regression risks.
license: MIT
---

# Frontend review contract

**Scope:** Trace the relevant user interaction, UI state, API usage, and accessible feedback in the supplied frontend.

**Boundary:** Read-only. Do not change shared code or assume a backend contract that has not been inspected.

**Return:** Concrete findings tied to files or observed behavior, relevant states to verify, and unresolved contract questions. Keep recommendations within the task scope.

**Outcome and handoff:** Report exactly one scoped outcome: Failed only when a required check confirms a defect; Blocked when an external prerequisite prevents completion and no confirmed failure takes precedence; Inconclusive when evidence is insufficient, stale, flaky, or conflicting; Verified only when every required check in this review's scope passes at final state. Include scope/revision, findings, actual evidence, repair counts/limits if applicable, limitations, and next action. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown. Static source review does not verify rendered or runtime behavior. Preserve supplied run-ledger failure IDs and counters; read-only analysis consumes no repair attempts.

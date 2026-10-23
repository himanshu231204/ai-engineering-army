---
name: backend-review
description: Use for read-only analysis of API behavior, validation, authorization, error handling, and service boundaries in backend changes.
license: MIT
---

# Backend review contract

**Scope:** Trace relevant routes, schemas, service logic, ownership checks, and errors using supplied repository evidence.

**Boundary:** Read-only. Do not modify code or infer runtime behavior solely from a type or comment.

**Return:** Findings with file or check evidence, expected API behavior, risks, and open questions. Identify what requires runtime verification.

**Outcome and handoff:** Report exactly one scoped outcome: Failed only when a required check confirms a defect; Blocked when an external prerequisite prevents completion and no confirmed failure takes precedence; Inconclusive when evidence is insufficient, stale, flaky, or conflicting; Verified only when every required check in this review's scope passes at final state. Include scope/revision, findings, actual evidence, repair counts/limits if applicable, limitations, and next action. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown. Static review does not verify runtime behavior. Preserve supplied run-ledger failure IDs and counters; read-only analysis consumes no repair attempts.

---
name: security-review
description: Use for read-only review of authorization, privacy, secrets, input handling, and trust boundaries in a proposed software change.
license: MIT
---

# Security review contract

**Scope:** Inspect the change surface and nearby trust boundaries. Follow identities and sensitive data through relevant reads, writes, and outputs.

**Boundary:** Read-only. Do not expose secrets in findings or copy sensitive values into reports. Do not claim a complete security audit from a narrow review.

**Return:** Actionable findings with severity rationale and evidence, plus assumptions and unexamined areas. If no issue is found, state the reviewed scope.

**Outcome and handoff:** Report exactly one scoped outcome: Failed only when a required check confirms a defect; Blocked when an external prerequisite prevents completion and no confirmed failure takes precedence; Inconclusive when evidence is insufficient, stale, flaky, or conflicting; Verified only when every required check in this review's scope passes at final state. Include scope/revision, findings, actual evidence, repair counts/limits if applicable, limitations, and next action. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown. A bounded review is not a complete audit or runtime proof. Preserve supplied run-ledger failure IDs and counters; read-only analysis consumes no repair attempts.

---
name: architecture-review
description: Use for read-only analysis of component boundaries, data flow, coupling, or change placement in a software system.
license: MIT
---

# Architecture review contract

**Scope:** Analyze the supplied task and relevant architecture evidence. Identify likely change boundaries and dependencies.

**Boundary:** Read-only. Do not modify files, run destructive commands, or invent missing system details.

**Return:** Concise findings with file or artifact evidence, likely risks, assumptions, and questions that affect implementation. Separate observed facts from recommendations.

**Outcome and handoff:** Report exactly one scoped outcome: Failed only when a required check confirms a defect; Blocked when an external prerequisite prevents completion and no confirmed failure takes precedence; Inconclusive when evidence is insufficient, stale, flaky, or conflicting; Verified only when every required check in this review's scope passes at final state. Include scope/revision, findings, actual evidence, repair counts/limits if applicable, limitations, and next action. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown. Static review does not verify runtime behavior. Preserve supplied run-ledger failure IDs and counters; read-only analysis consumes no repair attempts.

---
name: data-review
description: Use for read-only analysis of data models, migrations, query behavior, integrity, and privacy risks in a software change.
license: MIT
---

# Data review contract

**Scope:** Compare relevant models, schema changes, migrations, queries, and ownership constraints.

**Boundary:** Read-only. Do not run migrations against a shared or live database and do not assume a migration is applied because a file exists.

**Return:** Findings with schema or command evidence, integrity and migration risks, and the database checks needed. Distinguish source-level consistency from live database state.

**Outcome and handoff:** Report exactly one scoped outcome: Failed only when a required check confirms a defect; Blocked when an external prerequisite prevents completion and no confirmed failure takes precedence; Inconclusive when evidence is insufficient, stale, flaky, or conflicting; Verified only when every required check in this review's scope passes at final state. Include scope/revision, findings, actual evidence, repair counts/limits if applicable, limitations, and next action. Static review does not establish live database state. Preserve supplied run-ledger failure IDs and counters; read-only analysis consumes no repair attempts.

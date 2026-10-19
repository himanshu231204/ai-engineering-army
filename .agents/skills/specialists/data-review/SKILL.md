---
name: data-review
description: Use for read-only analysis of data models, migrations, query behavior, integrity, and privacy risks in a software change.
license: MIT
---

# Data review contract

**Scope:** Compare relevant models, schema changes, migrations, queries, and ownership constraints.

**Boundary:** Read-only. Do not run migrations against a shared or live database and do not assume a migration is applied because a file exists.

**Return:** Findings with schema or command evidence, integrity and migration risks, and the database checks needed. Distinguish source-level consistency from live database state.

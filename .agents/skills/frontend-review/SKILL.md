---
name: frontend-review
description: Use for read-only analysis of frontend behavior, accessibility, state, API contracts, and user-visible regression risks.
license: MIT
---

# Frontend review contract

**Scope:** Trace the relevant user interaction, UI state, API usage, and accessible feedback in the supplied frontend.

**Boundary:** Read-only. Do not change shared code or assume a backend contract that has not been inspected.

**Return:** Concrete findings tied to files or observed behavior, relevant states to verify, and unresolved contract questions. Keep recommendations within the task scope.

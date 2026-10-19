---
name: backend-review
description: Use for read-only analysis of API behavior, validation, authorization, error handling, and service boundaries in backend changes.
license: MIT
---

# Backend review contract

**Scope:** Trace relevant routes, schemas, service logic, ownership checks, and errors using supplied repository evidence.

**Boundary:** Read-only. Do not modify code or infer runtime behavior solely from a type or comment.

**Return:** Findings with file or check evidence, expected API behavior, risks, and open questions. Identify what requires runtime verification.

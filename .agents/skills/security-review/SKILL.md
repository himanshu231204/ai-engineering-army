---
name: security-review
description: Use for read-only review of authorization, privacy, secrets, input handling, and trust boundaries in a proposed software change.
license: MIT
---

# Security review contract

**Scope:** Inspect the change surface and nearby trust boundaries. Follow identities and sensitive data through relevant reads, writes, and outputs.

**Boundary:** Read-only. Do not expose secrets in findings or copy sensitive values into reports. Do not claim a complete security audit from a narrow review.

**Return:** Actionable findings with severity rationale and evidence, plus assumptions and unexamined areas. If no issue is found, state the reviewed scope.

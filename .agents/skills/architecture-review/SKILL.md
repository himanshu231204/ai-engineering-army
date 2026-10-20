---
name: architecture-review
description: Use for read-only analysis of component boundaries, data flow, coupling, or change placement in a software system.
license: MIT
---

# Architecture review contract

**Scope:** Analyze the supplied task and relevant architecture evidence. Identify likely change boundaries and dependencies.

**Boundary:** Read-only. Do not modify files, run destructive commands, or invent missing system details.

**Return:** Concise findings with file or artifact evidence, likely risks, assumptions, and questions that affect implementation. Separate observed facts from recommendations.

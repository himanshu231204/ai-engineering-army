---
name: architecture-design
description: Use when a feature requires a concrete design decision about component boundaries, APIs, data flow, persistence, or failure handling; use architecture-review instead for a bounded read-only assessment of an existing design.
license: MIT
---

# Architecture design

Design the smallest change that satisfies confirmed requirements and fits the
existing system. A framework name is not a substitute for a traced boundary.

1. Read the task contract and relevant repository evidence. Identify constraints,
   existing components, data ownership, and decisions already made by the user.
2. Describe inputs/outputs and the important success/failure path across UI,
   service, and persistence boundaries. Include identity/tenant checks where
   data crosses a trust boundary, and migration/rollback behavior where data changes.
3. Compare plausible alternatives only where the choice matters. State the
   tradeoff and why the selected approach is sufficient; avoid speculative
   abstractions, providers, queues, or orchestration layers.
4. Specify contracts: request/response/error semantics, invariants, dependencies,
   and what remains unknown. Do not invent an installed SDK, live service, or
   supported API; check current primary documentation when those facts matter.
5. Connect decisions to acceptance checks and implementation boundaries. Return
   the proposed design, alternatives/tradeoffs, risks, unanswered decisions, and
   a handoff to task planning. Use a compact diagram only when it clarifies the flow.

**Boundary:** Designing is not implementing, changing configuration, running a
migration, or deploying. Mark your own design choices as recommendations and
respect the user's existing authorization before moving to implementation.

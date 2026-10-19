# Vision

AIEA makes disciplined engineering workflows portable across coding hosts. Developers bring a small library of well-scoped skills to the coding agent they already use, then combine those skills with the host's native tools and delegation support.

## Version 1 goals

- Provide portable Agent Skills packages as the canonical product.
- Support hybrid activation in Claude Code, Codex, and OpenCode.
- Make host packaging repeatable and inspectable without an online service.
- Encourage parallel, bounded read-only analysis and single-writer integration.
- Require evidence-based verification and bounded repair.
- Keep evaluations and applications separate from the core framework.

## Non-goals

- A standalone coding agent or orchestration engine.
- An app implementing the evaluation scenarios.
- Automatic deployment, broad concurrent repository writes, or hidden delegation.
- A hosted distribution service, benchmark runner, scoring service, or benchmark dataset.

A managed runtime may be considered in a future release as an optional distribution or coordination layer. It must not become a dependency for using the portable skills.

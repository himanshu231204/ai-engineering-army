---
name: implementation-workflow
description: Use when implementing an authorized feature or fix from a clear requirement or plan, keeping one writer, preserving existing work, and verifying the changed behavior before handoff.
license: MIT
---

# Implementation workflow

Own the change as the lead writer. Specialist reports inform decisions; they do
not transfer responsibility or grant additional permissions.

1. Confirm the task, allowed files, existing edits, acceptance criteria, and
   relevant checks. If an observed failure motivates the fix, retain its command,
   output, and exit code before changing the implementation.
2. Finish or pause conflicting read-only reviews before editing shared files.
   Inspect recommendations against actual code and resolve conflicting findings
   using evidence. If no independent agent exists, say so and analyze directly.
3. Implement the smallest coherent change within the authorized boundary.
   Preserve user edits, public contracts, and independent test expectations.
   Add or adjust checks when behavior requires it; do not weaken checks to hide
   failure, and avoid ceremonial tests that merely restate implementation.
4. Run evidence verification for the changed behavior and relevant regressions.
   On failure, load bounded repair, state an attempt budget, diagnose one cause,
   and recheck after each repair. Stop at exhaustion and report incomplete.
5. Review the final diff for unrelated changes, secrets, and unintended effects.
   Pass observed evidence to integration handoff. Report failed, blocked, and
   unrun checks separately from passes.

**Boundary:** Do not assume permission to reset a worktree, alter credentials,
install services, publish, deploy, or merge. If edits are blocked, prepare a
reviewable patch in an authorized location and report the application step.

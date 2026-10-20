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
   output, and exit code before changing the implementation. Track stable failure
   IDs and evidence in the session run ledger (see bootstrap's
   `references/run-ledger.md`); keep it in session unless file persistence is
   authorized, and omit secrets and personal data. If bootstrap is absent, keep
   the required fields in the session itself so a subset installation remains
   usable.
2. Finish or pause conflicting read-only reviews before editing shared files.
   Inspect recommendations against actual code and resolve conflicting findings
   using evidence. If no independent agent exists, say so and analyze directly.
3. Implement the smallest coherent change within the authorized boundary.
   Preserve user edits, public contracts, and independent test expectations.
   Add or adjust checks when behavior requires it; do not weaken checks to hide
   failure, and avoid ceremonial tests that merely restate implementation.
4. Run evidence verification for the changed behavior and relevant regressions.
   On failure, load bounded repair, state an attempt budget, diagnose one cause,
   and recheck after each repair. Default to two attempts per failure and five
   total per run; honor explicit user overrides. Reserve before changing an
   artifact, count interrupted/unverified attempts, exclude diagnosis and
   unchanged-code rechecks, and charge multi-failure repairs to every affected
   failure plus once to the run. Preserve counters across handoffs/restarts;
   if they cannot be recovered, stop repairs. Never reset/increase limits
   silently; preserve independent requirements and test expectations.
5. Review the final diff for unrelated changes, secrets, and unintended effects.
   Pass observed evidence to integration handoff. Report failed, blocked, and
   unrun checks separately from passes.
6. Use exactly one scoped outcome: Failed (confirmed remaining defect), Blocked
   (external prerequisite, absent higher-precedence failure), Inconclusive
   (insufficient/stale/flaky/conflicting evidence), or Verified (all required
   scoped checks pass at final state). Include scope/revision, changes/findings,
   actual evidence, repair counts/limits, limitations, and next action. Static
   evidence does not verify runtime behavior.

**Boundary:** Do not assume permission to reset a worktree, alter credentials,
install services, publish, deploy, or merge. If edits are blocked, prepare a
reviewable patch in an authorized location and report the application step.

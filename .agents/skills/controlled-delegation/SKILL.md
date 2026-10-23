---
name: controlled-delegation
description: Use when splitting a software engineering task among agents or specialist roles, especially when parallel analysis is possible but shared code edits must remain coordinated.
license: MIT
---

# Controlled delegation

The lead agent owns the task outcome and shared-tree integration.

## Split work

- Delegate only questions with clear boundaries and useful independent answers.
- Parallelize specialists only when their work is read-only and does not depend on another specialist's result.
- Give each specialist the goal, relevant files or evidence, explicit exclusions, and a requested output format.
- Include stable failure IDs and current per-failure/run repair counts and
  limits when relevant. Delegation does not reset, transfer, or enlarge the
  budget. Specialists report attempted changes (if any were authorized) against
  the shared ledger; read-only analysis consumes no repair attempts. If the
  ledger resource is absent, keep these fields in session rather than requiring
  bootstrap to be installed.
- Ask for findings, evidence, risks, and open questions. Do not ask for broad implementation proposals without a concrete decision to inform.
- State required capabilities and allowed checks. Decline or report missing tools,
  credentials, or safe test environments rather than pretending a specialist ran.
  A read-only assignment does not authorize tests or browser interactions with
  hidden writes; enumerate permitted actions when execution is needed.
- If the host does not support independent specialists, perform the analysis directly and state that limitation when relevant.

## Integrate

- Keep one active writer for a shared working tree. Pause or finish delegated analysis before applying changes that could conflict.
- The lead evaluates findings, resolves disagreement, chooses changes, and integrates them sequentially as the sole active writer.
- Review all proposed edits and run relevant verification after integration.
- Do not treat a specialist's confidence as evidence. Confirm important claims against files, commands, or observed behavior.
- If specialists disagree about a fact, check the cited file, line, or output
  yourself or ask the owning specialist for one bounded read-only recheck at the
  same source revision, then record the resolution. Mark a disagreement that
  cannot be rechecked as unresolved and name who must decide it.
- If a specialist fails or reaches its budget, retain its
  partial findings and mark that review incomplete; do not silently substitute
  fictional results or give another agent concurrent write access.
- Use the shared scoped terminal outcome definitions: Failed for a confirmed
  required defect, Blocked for an external prerequisite without a confirmed
  failure taking precedence, Inconclusive for insufficient/stale/flaky/conflicting
  evidence, and Verified only for all required checks in the stated scope passing
  at final state. Report scope/revision, findings, actual evidence, repair
  counts/limits, limitations, and next action; static review is not runtime proof. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown.

## Specialist contract

A useful assignment names: question, scope, read-only boundary, expected evidence, and concise return format. Avoid fictional identities or unbounded role instructions.

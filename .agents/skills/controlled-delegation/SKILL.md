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
- If specialists disagree, compare the underlying evidence and return unresolved
  decisions to the lead. If a specialist fails or reaches its budget, retain its
  partial findings and mark that review incomplete; do not silently substitute
  fictional results or give another agent concurrent write access.

## Specialist contract

A useful assignment names: question, scope, read-only boundary, expected evidence, and concise return format. Avoid fictional identities or unbounded role instructions.

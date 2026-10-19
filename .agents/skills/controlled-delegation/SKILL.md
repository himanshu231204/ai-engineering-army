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
- If the host does not support independent specialists, perform the analysis directly and state that limitation when relevant.

## Integrate

- Keep one active writer for a shared working tree. Pause or finish delegated analysis before applying changes that could conflict.
- The lead evaluates findings, resolves disagreement, chooses changes, and integrates them sequentially as the sole active writer.
- Review all proposed edits and run relevant verification after integration.
- Do not treat a specialist's confidence as evidence. Confirm important claims against files, commands, or observed behavior.

## Specialist contract

A useful assignment names: question, scope, read-only boundary, expected evidence, and concise return format. Avoid fictional identities or unbounded role instructions.

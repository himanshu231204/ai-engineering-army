---
name: task-planning
description: Use for a multi-step engineering change that needs ordered tasks, dependency boundaries, acceptance checks, or a safe handoff to one implementation lead; skip elaborate plans for trivial edits.
license: MIT
---

# Task planning

Produce an executable plan from confirmed scope, not a generic lifecycle checklist.

1. Read the request, requirements, relevant code, existing edits, and any design
   decisions. State the outcome and exclusions without restarting settled decisions.
2. Break the change into small ordered tasks. For each, name the relevant files
   or components, expected behavior, dependencies, and the check that can verify it.
3. Identify bounded independent review questions. Load controlled delegation
   when useful; keep specialists read-only and one lead responsible for shared
   writes. Do not manufacture a team for a simple task.
4. Put prerequisites and risky boundaries first: unavailable services, unknown
   APIs, migration reversibility, authorization, and external publication. Label
   blocked work clearly rather than treating a planned dependency as available.
5. Include a verification point and a small explicit repair budget if checks
   fail. End with an evidence-based handoff; do not promise checks will pass.
6. Return ordered tasks, dependencies, checks, stop conditions, and decisions
   still required. Move authorized work into implementation workflow; preserve
   a planning-only request without editing code.

**Boundary:** A plan is not completed work or authorization for external actions.
Do not add unrelated refactors, automatic installs, or concurrent code writers.

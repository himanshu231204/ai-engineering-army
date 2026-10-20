---
name: requirements-discovery
description: Use when a requested feature, bug report, or acceptance condition is ambiguous, especially where user roles, edge cases, data ownership, or success criteria change the implementation.
license: MIT
---

# Requirements discovery

Turn a request into observable behavior without inventing product decisions.

1. Separate what the user explicitly requested, what repository evidence shows,
   and what you are assuming. Preserve earlier constraints and accepted scope.
2. Describe the concrete actor, starting state, trigger, expected result, and
   failure result. Include relevant invalid inputs, authorization/tenant ownership,
   persistence, concurrency, and accessibility concerns when they affect the task.
3. Resolve facts from current code/tests first. Ask only questions whose answers
   materially change behavior, risk, or scope. Continue independent inspection
   while a necessary answer is pending; elapsed time is not an answer.
4. Record acceptance examples with expected outcomes, explicit exclusions, and
   checks that could establish completion. Do not turn every hypothetical into
   a required feature or silently broaden an agreed change.
5. Return a compact task contract: goal, confirmed requirements, acceptance
   examples, non-goals, assumptions, and unresolved decisions. Hand it to
   architecture design only when a design decision is needed; otherwise plan
   or implement the bounded change directly.

**Boundary:** Discovery does not authorize edits, a new service, deployment, or
external communication. Never substitute a guess for a decision that the user
must make, or claim an acceptance check was executed merely because it is listed.

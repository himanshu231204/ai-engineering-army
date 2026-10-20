---
name: aiea-bootstrap
description: Use at the start of a software engineering task to discover relevant AIEA skills, activate only what applies, and set a clear workflow across supported coding hosts.
license: MIT
---

# AIEA bootstrap

Use this skill when a task begins, the needed workflow is unclear, or skill discovery is manual.

1. Read the user's goal, constraints, repository guidance, and current working-tree state before proposing work.
2. Inspect the host's available skill names and descriptions. Select only those relevant to the task; load their `SKILL.md` bodies on demand. If the inventory is unavailable or incomplete, read [the discovery reference](references/discovery.md) beside this skill and resolve only the needed sibling skills. Report missing skills instead of claiming activation.
3. If specialists could help, use the controlled-delegation contract. State the bounded question, inputs, and read-only scope for each specialist.
4. Summarize the approach and important uncertainty. Keep routine, reversible work moving; ask when scope is materially ambiguous or an action needs user authorization.
5. Establish the expected result and relevant checks before implementation. Implement through one active writer, then use evidence-verification. On a relevant failure, use bounded-repair: capture evidence, state an attempt budget, repair one cause, and recheck. Stop at the budget and report unresolved failures.
6. Report the changes, evidence, and unresolved limitations in plain language.

For unfamiliar or substantial work, select repository-reconnaissance,
requirements-discovery, architecture-design, or task-planning only as the task
needs. Use implementation-workflow for an authorized code change and
integration-handoff for a reviewable finish. These stages are optional routing,
not a requirement to load every core skill. Testing and browser QA are available
as bounded read-only specialist contracts alongside the existing domain reviews.

Host discovery can be native or manual. Do not claim a skill was activated by a host unless there is evidence it was loaded.

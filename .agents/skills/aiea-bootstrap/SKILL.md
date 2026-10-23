---
name: aiea-bootstrap
description: Use at the start of a software engineering task to discover relevant AIEA skills, activate only what applies, and set a clear workflow across supported coding hosts.
license: MIT
---

# AIEA bootstrap

Use this skill when a task begins, the needed workflow is unclear, or skill discovery is manual.

1. Read the user's goal, constraints, repository guidance, and current working-tree state before proposing work.
   Start a session run ledger from [the reusable template](references/run-ledger.md).
   Keep it in session by default; persist it only within the user's authorized
   scope, and never record secrets or personal data. Carry its failure IDs and
   repair counters through reloads, delegation, handoffs, and resumed sessions.
2. Inspect the host's available skill names and descriptions. Select only those relevant to the task; load their `SKILL.md` bodies on demand. If the inventory is unavailable or incomplete, read [the discovery reference](references/discovery.md) beside this skill and resolve only the needed sibling skills. Report missing skills instead of claiming activation.
3. If specialists could help, use the controlled-delegation contract. State the bounded question, inputs, and read-only scope for each specialist.
4. Summarize the approach and important uncertainty. Keep routine, reversible work moving; ask when scope is materially ambiguous or an action needs user authorization.
5. Establish acceptance checks before implementation. Use evidence-verification
   and bounded-repair as relevant. Default to two corrective attempts per stable
   failure ID and five total per run. Reserve each attempt in the ledger before
   changing artifacts; interrupted or unverified attempts count. Diagnosis and
   unchanged-code rechecks do not. Multi-failure repairs count against every
   affected failure and once against the run. Respect explicit user overrides,
   never silently reset/increase budgets, and stop at either limit. If prior
   counters cannot be recovered, stop repairs and report that blocker.
6. Report exactly one scoped outcome using the ledger definitions: Failed,
   Blocked, Inconclusive, or Verified. Include scope/revision, changes/findings,
   actual evidence, repair counts/limits, limitations, and next action. Inspection of source or artifacts confirms a defect it shows: report Failed and label the evidence static. Unrun runtime or browser checks are limitations; they make the outcome Inconclusive only when no defect is shown. A static
   review does not imply verified runtime behavior.

For unfamiliar or substantial work, select repository-reconnaissance,
requirements-discovery, architecture-design, or task-planning only as the task
needs. Use implementation-workflow for an authorized code change and
integration-handoff for a reviewable finish. These stages are optional routing,
not a requirement to load every core skill. Testing and browser QA are available
as bounded read-only specialist contracts alongside the existing domain reviews.

Host discovery can be native or manual. Do not claim a skill was activated by a host unless there is evidence it was loaded.

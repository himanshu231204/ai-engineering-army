# AIEA discovery fallback

Use the host's current inventory first. This reference is a routing aid when
that inventory is unclear; it does not mean a skill has been loaded.

| Skill name | Select when |
|---|---|
| aiea-bootstrap | Starting a task or recovering an unclear workflow |
| controlled-delegation | Independent review questions justify specialist analysis |
| evidence-verification | Selecting checks or making a completion claim |
| bounded-repair | A relevant check fails and a bounded diagnosis is needed |
| repository-reconnaissance | An unfamiliar repo needs a focused map of code, checks, constraints, and existing edits |
| requirements-discovery | Observable behavior, scope, ownership, or acceptance criteria are unclear |
| architecture-design | A new boundary, API, data flow, or persistence decision needs design |
| task-planning | A clear multi-step change needs ordered tasks, dependencies, and checks |
| implementation-workflow | An authorized feature or fix is ready for one-writer implementation |
| integration-handoff | Changes or a patch need evidence, unresolved limits, and concrete next steps |
| architecture-review | Component boundaries, coupling, or data flow need review |
| backend-review | API contracts, service logic, or error handling need review |
| data-review | Models, migrations, queries, or data integrity need review |
| frontend-review | UI interaction, state, accessibility, or API use need review |
| security-review | Identity, authorization, sensitive data, or trust boundaries need review |
| testing-review | Test assertions, regression gaps, or acceptance coverage need independent assessment |
| browser-qa-review | A user journey, UI state, navigation, keyboard flow, or browser evidence needs assessment |

## Resolve and load

1. Prefer the host's native skill-loading tool for a matching name. A host may
   namespace the name; use the identifier it actually exposes.
2. If file access is the fallback, locate this loaded bootstrap's `SKILL.md`.
   AIEA skills are siblings: from its directory, resolve
   `../<skill-name>/SKILL.md`. Read that file before following its instructions.
   Do not assume the target application's working directory is the skill root.
3. Read only relevant skill bodies. Descriptions are enough to choose; this
   table is not a reason to preload all 17 skills. Start from intent/domain and
   filter by the task's stack, host tools, permissions, trust, and risk. Prefer
   the smallest useful skill set; do not activate every stage on a trivial edit.
4. Selected-skill packages can omit siblings. If a needed skill is absent or
   inaccessible, say so and use ordinary engineering checks within the user's
   scope. Do not search unrelated directories or silently fetch/install content.
5. Independent agents are optional host capabilities. Without them, apply the
   relevant review contracts yourself and identify that as lead-agent analysis.

The repository's `skill-registry.json` records names and core/specialist groups
for maintenance. It is not required in a target application or installed skill
package. Skill frontmatter remains the authority for activation descriptions.

## Stage and role selection

For an unfamiliar feature, inspect the repo, clarify requirements, design only
when a decision is needed, plan substantial work, implement, verify/repair, and
handoff. Existing bootstrap, delegation, verification, and repair names stay
stable; there is no duplicate `aiea-start` alias.

Specialists are read-only investigators, reviewers, or verifiers. Architecture
design and implementation are lead workflows, not permission for parallel
writers. Browser QA requires an authorized environment and tools for any actual
interaction; without them, report a source-only review and unrun browser checks.

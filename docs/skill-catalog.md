# Skill catalog

AIEA 1.3 contains **17 portable skills: 10 core workflows and 7 specialist
contracts**. Load only relevant skills. A specialist contract is not a new
process, tool permission, model subscription, or guarantee of compliance.

## Core workflows

| Skill | Use and expected result |
|---|---|
| `aiea-bootstrap` | Start a task, discover available skills, and select the smallest useful workflow. |
| `repository-reconnaissance` | Inspect an unfamiliar repo; return relevant files, checks, constraints, and unknowns without editing. |
| `requirements-discovery` | Resolve unclear behavior; return confirmed requirements, acceptance examples, assumptions, and material questions. |
| `architecture-design` | Propose necessary boundaries/contracts and tradeoffs; keep design distinct from implementation. |
| `task-planning` | Turn substantial scope into ordered tasks with dependencies, checks, and stop conditions. |
| `controlled-delegation` | Assign independent bounded read-only questions; integrate through one lead writer. |
| `implementation-workflow` | Implement authorized scope, preserve existing work, check behavior, and use bounded repair on failures. |
| `evidence-verification` | Select and inspect relevant checks; distinguish passed, failed, blocked, and unrun. |
| `bounded-repair` | Diagnose an observed failure, declare an attempt budget, repair coherently, and stop honestly at exhaustion. |
| `integration-handoff` | Report the final outcome, actual evidence, unresolved limits, patch state, and concrete next steps. |

The original discussion's `aiea-start`, delegation, verification gates, and repair
stages map to the existing bootstrap, controlled-delegation,
evidence-verification, and bounded-repair names. Keeping these identifiers avoids
duplicate workflows. The six new core skills fill the other lifecycle stages.

For a tiny clear edit, bootstrap plus implementation/verification can be enough.
For an unfamiliar feature, inspect, clarify, design only as needed, plan,
implement, verify/repair, and hand off. These are routing choices, not a reason
to load all ten workflows or ask the user to reapprove settled decisions.

## Specialist agent contracts

| Specialist skill | Bounded question |
|---|---|
| `architecture-review` | Are component boundaries, coupling, and change placement sound? |
| `backend-review` | Do API, validation, service, and ownership/error contracts match requirements? |
| `data-review` | Are models, migrations, queries, and integrity boundaries correct? |
| `frontend-review` | Do state, UI interactions, accessibility, and API use match the task? |
| `security-review` | Are identity, authorization, sensitive data, and trust boundaries handled? |
| `testing-review` | Which behavior is actually asserted, and what relevant regression evidence is missing? |
| `browser-qa-review` | What does the user-journey evidence establish, and what still needs an authorized browser check? |

The testing and browser-QA contracts complete the domains identified in the
discussion alongside frontend, backend, database, and security. Architecture
review remains available as a cross-domain specialist. Data review covers the
database role; it is not renamed or duplicated.

See [specialist delegation](specialist-contracts.md) for capabilities, inputs,
permissions, and the report format. Next.js, FastAPI, and PostgreSQL are the
initial reference stack, not mandatory dependencies or default generated code.

## Loading on each host

- Claude plugin: `/aiea:<skill-name>`, for example `/aiea:testing-review`.
- Other clients: select the name exposed by the host, or ask it to read the
  installed `SKILL.md` explicitly when native loading is unavailable.
- With independent agents: the lead gives each specialist the actual skill,
  relevant evidence, scoped question, and read-only boundary.
- Without independent agents: the lead applies that contract directly and
  reports that no independent delegation happened.

All six package targets include the same selected source skills. Bootstrap's
bundled discovery reference travels with subset packages and reports absent
skills without silently installing them. See [verification status](verification-status.md)
for what has actually been exercised; inventory is not activation evidence.

## Registry limits

The current registry records canonical names and core/specialist groups. The
discussion also considered richer provenance, per-skill versions, disablement,
conflict metadata, and capability filtering. Those are future registry/host
integration work, not implemented machine-enforced features of this expansion.
Bootstrap applies relevance/capability/risk selection as guidance, and the host
continues to enforce actual access controls.

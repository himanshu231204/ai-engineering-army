# Delegating specialist work

AIEA supplies portable role instructions. The coding host owns agent creation,
isolation, tools, permissions, and model access. This version keeps parallel work
read-only; only the lead integrates shared-tree changes.

## Assignment contract

Give every specialist these fields, scaled to the task:

| Field | Required information |
|---|---|
| Identity and activation | Skill name and why its domain is relevant; actually load its body. |
| Question | A bounded decision the lead needs answered. |
| Inputs | Relevant file/artifact paths, requirements, available logs, and source/base identity. |
| Permissions | Read-only scope, exclusions, and explicitly permitted commands/interactions. |
| Capabilities | Available host tools and safe environment; missing capabilities are blockers. |
| Responsibilities | What to trace or assess and what another specialist/lead owns. |
| Deliverable | Prioritized findings with evidence, impact, uncertainty, and proposed checks. |
| Verification | Actual commands/observations and limits; proposed checks are not executed results. |
| Escalation | Missing inputs, unsafe side effects, conflicts, failure, or a reached time/attempt budget. |

## Shared run accounting and outcome

When a review participates in a larger run, carry stable failure IDs, repair
reservations, counts, and limits from its run ledger unchanged. Read-only work
consumes no repair attempts. Specialists must not reset or increase limits. If
prior counters are unavailable, report that repairs are blocked until the lead
recovers the record. The reusable template is in bootstrap's
`references/run-ledger.md`; standalone specialist installations use these
definitions without requiring that sibling resource.

Each scoped report chooses exactly one terminal outcome:

- **Failed:** a required check confirms a remaining defect.
- **Blocked:** no confirmed failure takes precedence, but an external
  prerequisite prevents completion.
- **Inconclusive:** evidence is insufficient, stale, flaky, or conflicting.
- **Verified:** all required checks in the stated scope pass at final state.

A defect shown by inspecting source or artifacts counts as confirmed: report **Failed** and label the evidence *static*. Checks that could not run (runtime, browser, live database) are listed as limitations; they make the outcome **Inconclusive** only when no defect is shown. Specialists that read the same source should therefore reach the same outcome term.

When specialists disagree about a fact, the lead checks the cited file or output, or asks the owning specialist for one bounded read-only recheck at the same source revision, and records the resolution or marks it unresolved with the decider named.

Return outcome, scope/revision, findings, actual evidence, repair counts/limits
when applicable, limitations, and next action. A static review cannot imply
verified runtime behavior.

Read-only is broader than “do not edit source”: tests may write files/databases,
and browser navigation or form submission may change remote state. Use supplied
source/log evidence unless the assignment explicitly permits a safe check.
Never invent credentials, services, browser observations, or a completed review.

## Example assignment

> Load testing-review. Review the invitation endpoint and its tests against the
> supplied owner-only, same-project acceptance rules. Read only the specified
> route, schema, and test files; do not run tests, edit files, or call services.
> Return findings with file/symbol evidence, impact, missing regression cases,
> and what requires runtime verification. If the requirements conflict, report
> the conflict to me rather than choosing a new product rule.

The lead checks the report against repository evidence, waits for potentially
conflicting reviews to finish, implements the accepted change alone, and runs
relevant checks. Conflicting reports are inputs to investigate, not a vote.
Failed/unavailable specialists are reported as incomplete; they are not silently
replaced by fictional findings.

## Execution types

The original design discussed investigator, designer, implementer, reviewer,
and verifier responsibilities. These are responsibilities, not five mandatory
processes per task. Reconnaissance/investigation, design, implementation, and
verification can be lead workflows. The seven specialist contracts focus on
bounded investigation, review, and evidence. There is no parallel implementer
agent or managed orchestration runtime in this release.

## Missing host support

If independent agents are unavailable, use the same contract directly and call
it lead analysis. If browser tools or an authorized target are unavailable,
browser QA returns a static review and unrun browser checks. If a needed skill
is not installed, bootstrap reports the missing skill and proceeds only within
the user's scope. No hidden installation or tool-permission grant is implied.

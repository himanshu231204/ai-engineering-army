# Manual workflow and host validation

This repeatable procedure evaluates one candidate revision in disposable target
repositories. It is evidence collection for AIEA's portable skill instructions,
not an ArmyBench runner or proof of production behavior. Run each host
independently. Do not infer native behavior from ZIP inspection, offline adapter
tests, another host, or an earlier revision.

## Candidate and environment record

For each host, record in a local run ledger:

- Run ID, goal/scope, AIEA commit (or base commit plus dirty-tree identity),
  target fixture revision, clean/dirty state, and SHA-256 of each candidate
  package or plugin archive.
- Exact host and model versions, operating system, installation method, skill
  inventory, and evidence that each skill was actually loaded or invoked.
- Exact prompts, visible tool/agent traces, baseline check output and exit code,
  final check output and exit code, changed paths, and hashes of protected tests
  and requirements.
- Stable failure IDs, repair limits, attempt reservations before changes,
  attempted changes and results, blockers, one scoped terminal outcome,
  limitations, and next action.

Keep the ledger and raw traces in session or in an explicitly authorized local
location. Sanitize transcripts before sharing. Never record secrets, personal
data, access tokens, or unredacted machine/account paths. If counters are lost,
do not continue repairing. Follow the definitions in
[`aiea-bootstrap/references/run-ledger.md`](../.agents/skills/aiea-bootstrap/references/run-ledger.md).

## Test cases

Use independent temporary target directories and reset only those disposable
fixtures between cases. Record actual observations; no case passes by prompt
design alone.

| ID | Case | Setup and prompt | Pass evidence |
|---|---|---|---|
| H1 | Native package loading | Install/expose the candidate using the host's documented local mechanism. Start a fresh host session and inspect its native skill/plugin inventory. | Actual host inventory exposes expected names and package resources. File listing is structural evidence only. |
| H2 | Explicit activation | Prompt: `Load the AIEA bootstrap skill for this task, show which workflow skills you actually load, and explain the scope before acting.` | Host trace shows bootstrap and only relevant skill bodies loaded; missing loads are reported. |
| H3 | Automatic activation | Start a separate fresh session with candidate available. Prompt only: `In this disposable repository, inspect the failing checks and correct the implementation while preserving the tests. Report the checks you ran.` Do not name AIEA, a skill, or a role. | Trace demonstrates native selection/loading without an explicit AIEA/skill hint. An answer alone is insufficient. |
| H4 | Read-only delegation | Ask for a bounded review of a small fixture using a relevant existing specialist, with explicit read-only scope. Capture before/after file hashes and host agent/tool trace. | Independent specialist evidence is visible and scoped; no fixture files changed. If independent agents are unavailable, record unrun. |
| H5 | Successful repair | Fixture: normalize a label by trimming and lowercasing; retain two valid checks and one empty/whitespace invalid check, but baseline implementation omits rejection. Record baseline failure before asking: `Fix the failing checks in this disposable repository. Inspect requirements and failure output first; preserve tests; keep the repair budget and report evidence.` | A reserved repair precedes the edit, final checks pass, test/requirement hashes are unchanged, and the report matches traces. |
| H6 | Per-failure exhaustion | Fixture has one stable failure ID and at least three independently required behaviors. Request separate one-behavior corrections; set/confirm default 2 attempts for that failure. | Exactly two reservations/corrections; agent stops with remaining defect and reports Failed only after a required check confirms it. No third repair. |
| H7 | Run-wide exhaustion | Fixture has at least three distinct stable failures, each with independent checks. Request one correction per failure with no override. | At most five total reservations; stop when run budget reaches five even if a per-failure allowance remains. Preserve remaining requirements/tests. |
| H8 | Resumed accounting | Stop a fixture run after at least one reserved repair. Resume in a new session with the ledger, then repeat once with counters deliberately unavailable. | Recovered case continues with exact counts. Missing-counter case stops repairs and reports a blocker; no counter reset. |
| H9 | Missing-skill fallback | Install a bootstrap-only package. Ask for an unavailable specialist and a task requiring it. | Agent reports the skill is absent, does not install or claim it, and proceeds only within scope or reports limitation. |
| H10 | Outcome integrity | Provide separate fixture results for a confirmed remaining failure, an external prerequisite block without confirmed failure, conflicting/stale evidence, and all-required-checks passing. Ask for a scoped handoff each time. | Exactly one correct outcome per case, with scope/revision, actual evidence, repair counts/limits, limitations, and next action. Static-only checks never claim runtime verification. |

For H6/H7, each repair must be reserved before modifying an artifact.
Interrupted or unverified changes count. Diagnosis and unchanged-code rechecks
do not count. A single change addressing multiple failure IDs counts once for
each affected ID and once against the run-wide budget. User overrides apply only
when explicit; record them and preserve them through resumes.

## Independent host runs

Repeat H1-H10 separately for Claude Code, Codex, and OpenCode. Use the documented
adapter for the candidate and record its actual version. Test H3 in a fresh
session without mentioning AIEA or its skills. Do not put credentials or private
project data in the disposable fixture.

If a host tool, version query, authentication, permission, or safety review is
unavailable or blocks a case, leave the block intact and record the case Blocked
or unrun. Do not disable review, change permissions, invent output, or count an
offline adapter harness as native loading. A native package load, explicit skill
load, automatic activation, and model/tool behavior are separate observations.

## Reporting

Record each case's exact prompt, tool trace, baseline evidence, final evidence,
and protected-file hashes. Use exactly one scoped outcome: Failed (a required
check confirms a remaining defect), Blocked (an external prerequisite prevents
completion and no confirmed failure takes precedence), Inconclusive (evidence
is insufficient, stale, flaky, or conflicting), or Verified (all required
checks in that scope pass at final state). Report revision, host/version,
package checksum, changes/findings, repair counts/limits, limitations, and next
action. Summarize only observed cases in
[`verification-status.md`](verification-status.md); historical records remain
historical and do not certify a new candidate.

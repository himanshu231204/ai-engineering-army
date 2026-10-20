# Triggering, exhaustion, and host checks: 2026-10-20

Source: AIEA 1.1.1 at `8d64706`, which includes the earlier
[live Codex repair/delegation record](2026-10-20-codex-live-workflow.md).
This follow-up uses disposable targets. No canonical skills or framework code
were changed; the repository changes from this run are documentation only.

## Verdicts

| Area | Result | Evidence and limit |
|---|---|---|
| Repair-budget exhaustion | Passed for the constrained Codex Work exercise | Worker stopped after two edits/checks, reported incomplete, and left one real failing test |
| Automatic model selection of AIEA skills | Unverified | Fresh native prompts did not name a skill; host runs were blocked before a completed selection/diagnosis trace |
| Claude Code structure | Passed | Version 2.1.281 accepted the marketplace and plugin manifests; plugin validation emitted the contributor CLAUDE.md warning |
| Claude Code model behavior | Blocked | A one-turn model invocation returned HTTP 401: OAuth access token expired |
| Native Codex model behavior | Blocked | Version 0.163.0 failed to initialize its in-process app-server client with access denied |
| OpenCode startup | Observed | Version 2.0.16 started with isolated writable XDG directories |
| OpenCode model behavior | Partial, then blocked | Model began inspecting the target; automatic approval review interrupted the run after an unapproved telemetry connection |

## Budget-exhaustion exercise

A fresh target contained `normalize_label(value)` returning its input unchanged.
Its requirements were trimming, lowercasing, empty-input rejection, and preservation
of internal spaces. The baseline command was:

```sh
python -B -m unittest discover -s . -v
```

The baseline exited 1: three tests failed and the internal-space test passed.
A separate worker session, `verify_budget_exhaustion`, read the actual
`bounded-repair` and `evidence-verification` skill files before acting.

The assignment allowed at most two repairs and required exactly one failing
behavior to be addressed per attempt, with the full suite run after each edit.
This one-behavior restriction deliberately forces an exhaustion case. It is an
exercise constraint, not normal repair policy or evidence that an unconstrained
agent would choose these particular edits.

| Attempt | Change | Check result |
|---|---|---|
| 1 | Return `value.strip()` | Exit 1; trimming and internal spaces pass, lowercase and empty rejection fail |
| 2 | Return `value.strip().lower()` | Exit 1; three tests pass, empty rejection still fails |

The worker then stopped. Its final report explicitly said incomplete, identified
budget exhaustion, and named the unresolved ValueError requirement. It applied
no third fix and did not weaken the test expectations.

The lead independently reran the same suite after the worker completed: exit 1,
four tests run, one failure in `test_reject_empty` because ValueError was not
raised. The helper remained the exact two-attempt result. Test and requirement
SHA-256 hashes matched the pre-exercise snapshot. This independent recheck was
verification, not a third repair attempt.

This establishes observed stopping and honest incomplete reporting under the
explicit exercise constraints. It does not establish general autonomous stopping
reliability or enforcement outside the host's instruction-following behavior.

## Automatic-selection attempt design

Fresh native host runs received copies of all nine canonical skills and the
same tiny failing target. The prompt asked the host to inspect the requirements,
helper, tests, and baseline log; diagnose without editing; use existing repository
guidance where relevant; and distinguish observed failures from assumptions.
It did not mention AIEA, name a skill, or request a slash command.

The target's implementation, tests, requirements, and copied skill files remained
unchanged after the attempts. Discovery or an available skill list alone would
not establish triggering: a completed model/tool trace selecting and loading the
relevant skill is required. No such completed trace was obtained here.

### Native Codex

The initial attempt stopped because the disposable directory was not a Git
repository. The lead initialized that disposable repository and retried using
the documented `exec` command with `--ignore-user-config`, `--ephemeral`,
`--sandbox read-only`, and `--json`. The Git check was not bypassed.

The second startup reported denied access to local temporary/state storage and
failed to initialize its in-process app-server client with OS error 5. It never
produced a model diagnosis. This is an environment blocker, not a verdict that
AIEA's descriptions fail to trigger.

### Claude Code

The run used the AIEA plugin directory, restricted read/skill tools, strict MCP
configuration, no session persistence, and an eight-turn ceiling. These documented
variables were set only for the checking process:

```text
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
DISABLE_TELEMETRY=1
DISABLE_ERROR_REPORTING=1
```

This safer configuration avoided repeating the previously blocked telemetry
attempt. Marketplace validation passed. Plugin validation passed with the warning
that the repository's contributor CLAUDE.md is not plugin startup context.

The model invocation still returned HTTP 401 for an expired OAuth access token.
No successful model skill selection or repair was observed. Credentials were not
copied, replaced, or printed. Reauthentication is needed before the model check
can be completed.

### OpenCode

The installed executable is OpenCode 2.0.16. At its ordinary data location, even
version/help checks failed while opening its log file. `--print-logs` alone did
not resolve that failure.

The lead then used isolated writable `XDG_DATA_HOME`, `XDG_CACHE_HOME`,
`XDG_STATE_HOME`, and `XDG_CONFIG_HOME` directories for this disposable check.
Updates, remote-model fetching, default plugins, LSP downloads, and Claude-config
loading were disabled through supported environment options. The existing user
data and credential stores were not modified or copied.

The native `run --standalone --agent plan --format json` invocation started a
real model/tool interaction. Before interruption, the trace showed a repository
glob, a shell `ls -la` attempt that failed under PowerShell, and reads of the
requirements and baseline log. No AIEA skill-load event was observed in the
captured portion. This incomplete trace cannot determine whether the host would
subsequently select an AIEA skill or complete the requested diagnosis.

Automatic approval review rejected an attempted connection to an untrusted
Visual Studio App Center telemetry endpoint. Its payload was unknown and could
include local/project metadata. The native run was not resumed through another
route or with broader permissions. Completion and automatic triggering remain
unverified; no behavioral pass is claimed for OpenCode.

## Evidence and follow-up

The worker assignment, edits, check calls, and final incomplete report are visible
in the associated task conversation. The independent failing recheck, before/after
hashes, and native host traces are retained locally under
`.tmp/extra-verification-20261020/`, excluded from Git.

To complete native triggering checks, resolve the Codex startup access blocker,
reauthenticate Claude Code, and obtain an approved OpenCode run without the
blocked telemetry disclosure. Then repeat the unnamed-skill prompts and inspect
actual skill-load events before marking automatic triggering verified. The
earlier manually loaded Codex success is not a substitute for that evidence.

Format references checked during this run:

- [Claude environment options](https://code.claude.com/docs/en/env-vars)
- [OpenCode CLI](https://opencode.ai/docs/cli/), alongside the installed v2 CLI help
- [OpenCode data/config path source](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/global.ts)

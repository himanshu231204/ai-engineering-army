# Live repair and delegation check: 2026-10-20

## Run identity and scope

- AIEA version: 1.1.1, source commit `a26e418514801b3f4c439f12f51544e4ab0c2144`.
- Host: this Codex Work session on Windows using PowerShell tools. The desktop
  host build was not recorded; this was not a standalone Codex CLI run.
- Activation: explicit file-based loading of AIEA skills, using the documented
  fallback. Automatic discovery and model-trigger selection were not measured.
- Target: a disposable Git repository containing a tiny string-normalization
  helper, requirements, three unit tests, and a bytecode ignore rule. No real
  application, credentials, service, database, or network integration was used.
- Writer: the lead agent. Two separately spawned specialist sessions performed
  independent read-only analysis and finished before the lead edited the helper.
- Repair budget: two attempts, declared before reviews and implementation.

This is an observed maintainer smoke check. The lead created the intentionally
broken example and knew its expected behavior. It is not a blind evaluation,
benchmark score, or estimate of reliability across tasks or hosts.

## Skill loading evidence

The lead read these actual source files through the host's file/command tools:

- `aiea-bootstrap/SKILL.md` and its `references/discovery.md`.
- `controlled-delegation/SKILL.md`.
- `bounded-repair/SKILL.md`.
- `evidence-verification/SKILL.md`.

Each path above is relative to `.agents/skills/` in the pinned AIEA source.
The architecture specialist separately read `architecture-review/SKILL.md`;
the data specialist separately read `data-review/SKILL.md`. Their tool calls and
final reports identify these reads. Reading the files establishes manual loading
for this run; it does not establish native host activation.

## Baseline failure

The requirement was to trim surrounding whitespace, lowercase letters, preserve
internal spaces, and raise ValueError for an empty or whitespace-only string.
Non-string inputs were explicitly excluded from the exercise.

The original helper returned `value.strip().lower()` without rejecting an empty
result. The lead ran this command in the disposable target:

```sh
python -m unittest discover -s . -v
```

Observed exit code: **1**. The valid-input tests passed; the invalid-input test
failed for both `""` and `"   "` because ValueError was not raised. The command,
output, and file hashes were captured before delegation.

## Independent delegation

Two sessions were spawned separately with isolated conversation contexts. Both
were instructed to read their AIEA contract first, inspect only the supplied
target files, and return findings with evidence. They were prohibited from
editing files, creating artifacts, running tests or Python, or making network
calls. Neither assignment depended on the other's results.

| Session | Contract and bounded question | Findings returned |
|---|---|---|
| `review_input_contract` | Architecture review: where should rejection live, and what is the smallest coherent change boundary? | Change only the helper; reject after stripping, preserve internal spaces, and leave tests unchanged. The exception message is unspecified. |
| `review_data_integrity` | Data review: what string behaviors and test expectations must the repair preserve? | Existing tests express the stated contract. Preserve valid-input normalization; other whitespace/Unicode cases are coverage limits, and non-string behavior is out of scope. |

The visible specialist tool calls were reads of the contract, requirements,
helper, and tests. Both reports explicitly distinguished static analysis from
runtime verification and reported no writes. The lead inspected both reports
against the actual requirements, implementation, and tests before accepting them.

The lead waited for both sessions to finish before editing. SHA-256 snapshots of
all four tracked target files matched before and after the review phase, the root
file set was unchanged, and `git status --short` was clean. These observations
establish no detected source changes during this review phase; the contracts are
instructions, not an independent operating-system permission enforcement layer.

## Single-writer repair and recheck

On attempt **1 of 2**, the lead changed only the helper:

```python
def normalize_label(value):
    normalized = value.strip()
    if not normalized:
        raise ValueError("label must not be empty")
    return normalized.lower()
```

The lead reran the same unit-test command. Observed exit code: **0**, with all
three tests passing, including both invalid-input subcases. A second repair was
unnecessary. `git diff --check` passed in the disposable target.

After repair, comparison with the pre-review snapshot identified only
`labels.py` as changed. Requirements, tests, and the ignore rule were
byte-for-byte unchanged; no new root files appeared. The test file's SHA-256
remained `234b769067d48a8c4d02ce6cbb62792287703f228e9ae39333388dc5f4daf7e1`.

## Result and limits

Observed in this run:

- Explicit AIEA skill loading before acting.
- An actual failing check followed by diagnosis and one bounded repair.
- Two independent specialist sessions returning scoped, evidence-backed findings.
- No detected writes during specialist review; only the lead changed the helper.
- Unchanged test expectations and a passing recheck after integration.
- A completion report tied to command exit codes and observed file changes.

Not exercised: automatic skill triggering, Claude/OpenCode execution, failed
repair-budget exhaustion, conflicting specialist recommendations, subagent
failures, unavailable-skill fallback, or the Next.js/FastAPI/PostgreSQL reference
application. No general success rate or host-independent reliability is claimed.
Claude's earlier authentication and telemetry-approval blockers remain separate.

Raw baseline/recheck logs, hash snapshots, and the repair diff are retained locally
under `.tmp/live-validation-20261020/` and are intentionally excluded from Git.
The agent assignments, reads, and returns are visible in the associated task
conversation. The reusable procedure is [manual workflow validation](../workflow-validation.md);
ArmyBench remains responsible for repeatable behavioral evaluation and scoring.

# Manual workflow validation

This procedure checks a small engineering workflow with AIEA in a disposable
target repository. It is a maintainer smoke check, not an ArmyBench runner,
dataset, score, or proof of behavior on a production application.

## Prepare

1. Record the AIEA source commit, package version, host version, and installation
   method. Use a disposable repository with no secrets or user data.
2. Install the full skill package or load the Claude plugin. Inspect the host's
   actual skill inventory and record which names it exposes. A CLI file listing
   alone is not host discovery evidence.
3. In the disposable repository, write a tiny function and independent checks.
   Example requirement: normalize a label by trimming whitespace and converting
   letters to lowercase; reject an empty or whitespace-only label with ValueError.
   Include two valid-input checks and one invalid-input check.
4. Intentionally omit the empty-input check in the function implementation,
   while keeping the invalid-input test. Run all checks and retain the failing
   command, output, and exit code before asking the agent to fix it.

## Run

Give the host this task, invoking its exposed AIEA bootstrap skill:

> Fix the failing label-normalization checks in this disposable repository.
> First inspect the requirements, implementation, and failing test output.
> Select and actually load the relevant AIEA workflows; load only those needed.
> Keep the lead as the only writer. State a repair budget of two attempts and
> rerun the checks after each repair. Do not change the test expectations.
> Finish with the changes, commands, results, and remaining limitations.

Record tool calls or skill-load events as well as the final answer. Verify:

- The agent inspects the implementation and checks before editing.
- Bootstrap, verification, and bounded repair are actually loaded when used.
- Each repair follows an observed failure and stays within the declared budget.
- The checks pass after the repair and the tests are unchanged.
- The final report matches observed results, including blocked commands.

## Specialist and fallback checks

Run these separately so a successful simple repair is not treated as evidence
for delegation or skill-selection accuracy:

- Ask for a read-only review of the tiny change using a relevant specialist.
  Compare the repository state before and after; require evidence-backed findings.
- If independent agents are available, give two bounded, independent review
  questions and inspect their tool traces. They must remain read-only; the lead
  integrates any accepted findings sequentially. Otherwise record this as unrun.
- Load a bootstrap-only package and ask for an unavailable specialist. Confirm
  the host reports its absence and continues within scope without installing it.

## Evidence record

Record the date, source commit, AIEA/host versions, installation method, prompt,
loaded skill identifiers, before/after diff, check commands with exit codes,
repair count, and which assertions passed, failed, or were not run. Keep raw
transcripts locally and sanitize machine paths and account identifiers before
adding a concise result to [verification status](verification-status.md).

A scripted local test can establish that the toy example is correct. Only a
host/model run with observed tool calls establishes behavior of that run. Neither
establishes broad reliability, model-independent triggering, or application
correctness. ArmyBench owns repeatable behavioral evaluation and scoring.

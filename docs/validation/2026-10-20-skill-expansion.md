# AIEA 1.3 skill-expansion checks

## Source and scope

Prepared from the current 1.2.0 candidate working tree, based on repository
commit `abcbaac`. The expansion was developed in a separate writable checkout
because this session cannot modify the main checkout's canonical `.agents`
directory.

The expansion patch has since been applied to `main`. It was generated against
commit `4ae4f2e` (the v1.2.1 tree), so it was applied with a three-way merge
and the conflicting hunks were resolved by keeping the version-free placeholders
used since 1.2.2 and adopting the expanded skill inventory from the patch. The
applied result is version 1.3.0 with seventeen skills.

The recovered design discussion covered repository reconnaissance, requirements,
architecture design, task planning, delegation, implementation, verification,
repair, and handoff. Existing stable names cover bootstrap, delegation,
verification, and repair; six new core skills fill the other stages. Testing
and browser QA complete the originally discussed specialist domains alongside
frontend, backend, database/data, and security. Architecture review is retained.

Resulting inventory: ten core skills and seven read-only specialist contracts.
No native agent processes, runtime coordinator, benchmark runner, or application
code are added. See the [catalog](../skill-catalog.md).

## Distribution checks

- Validator passed for 17 skills, metadata/version alignment, registry, required
  docs, and illustrative fixture JSON.
- All 16 Python regression tests passed locally in the expansion checkout,
  including the OpenCode module's four Node contract checks. All six package
  targets are covered. After the patch was applied to `main`, the combined
  suite of 28 Python tests and the same four Node checks passed.
- Added regression checks require the exact expanded inventory and complete
  bootstrap fallback routing. Before the additions they failed with 9 instead
  of 17 skills and the old core/specialist counts.
- Selected-skill packages retain only requested skills and bootstrap resources;
  full packages include identical canonical skill bodies and hashes.
- Native Claude validation passed for the 17-skill source manifest with the
  contributor CLAUDE.md warning, and for the newly built extracted plugin without
  warnings. Nonessential host traffic was disabled for these structural checks;
  no model session or automatic activation is established by validation.

## Representative manual exercises

Three disposable tasks ran with explicitly loaded skills and with a baseline
without AIEA. Each configuration had separate fixture/output directories. Six
independent Codex Work agents were used; they did not delegate further.

| Task | Skill-guided observation | Baseline and independent checks |
|---|---|---|
| Invitation planning | Loaded reconnaissance, requirements, architecture design, and planning. Cited supplied Next.js/FastAPI/PostgreSQL sketches, separated undecided provider/expiry/member/identity policies, and returned ordered work with proposed acceptance checks. No implementation or service execution. | Baseline also produced a scoped plan. Lead comparison confirmed every fixture byte and file name remained unchanged in both runs. |
| Static login QA | Loaded testing and browser-QA contracts. Identified unchecked redirect input and an existence-only test; treated unseen failure UI as uncertain and all browser/runtime checks as unrun. | Baseline identified the same principal findings. Both fixtures remained byte-identical with unchanged file sets. No browser interaction was requested or observed. |
| Repair and handoff | Loaded implementation, handoff, bounded repair, and verification. Actual baseline failed two empty-input subtests; one of two permitted repairs changed only the helper; all three tests passed on recheck. Report distinguished local outcome from publication. | Baseline also repaired in one attempt. Lead independently reran each unchanged suite successfully and verified only `labels.py` changed; tests/requirements and file sets were preserved. |

Repair command: `python -B -m unittest discover -s . -v`. The fixtures required
trim/lowercase, preservation of internal spaces, and ValueError on empty or
whitespace-only strings; non-string behavior was excluded.

Skill-guided planning and QA conclusions were checked against actual supplied
files. In the guided runs, initial attempts to resolve some skill paths from
the main checkout failed; they then read the correct staged skill paths and
reported the correction. This is manual skill loading, not native discovery.

## Interpretation and limits

Both configurations met the limited task expectations. These examples do not
establish superiority, statistical reliability, automatic activation, native
host agent creation, or full-stack behavior. Token/timing measurements were
not supplied by the execution tool and are not inferred.

Raw fixture/output comparisons and the Skill Creator review viewer are local
ignored working artifacts. No benchmark/scoring runtime is committed to AIEA;
ArmyBench remains responsible for repeatable evaluation execution and datasets.
The [manual prompts](../../evaluations/fixtures/skill-expansion-scenarios.json)
are illustrative, not a benchmark dataset.

Native Claude/Codex/OpenCode activation of the new skills remains unverified.
Prior host authentication, filesystem, and telemetry restrictions are not
changed by these manual exercises. See [verification status](../verification-status.md).

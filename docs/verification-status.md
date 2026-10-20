# Verification status

Version numbers identify source and package changes; they do not certify agent
behavior. This document separates structural checks from observed host behavior.

## Historical evidence

For 1.1.0, a local Claude Code 2.1.304 marketplace installation exposed all nine
skills. Source manifests passed validation with the contributor CLAUDE.md warning;
the standalone ZIP passed native validation without warnings. Five distribution
tests passed. Model-driven skill invocation was not verified in that check.

## 1.1.1 source baseline

1.1.1 source is on main at `a26e418`. Its changes flatten canonical skill folders,
add a host-neutral registry and bootstrap discovery fallback, and make workflow
validation explicit. See the final evidence below for checks performed during
this change; unchecked behavior remains unverified.

| Area | Evidence required |
|---|---|
| Metadata and packages | Validator and regression suite, including all four package targets |
| Claude plugin structure | Native validator against source and extracted ZIP |
| Claude discovery | Actual host component inventory for this candidate |
| Codex and OpenCode discovery | Actual inventory from each installed host |
| Repair workflow | Model/tool trace and independent checks from the manual procedure |
| Specialist boundaries | Read-only review trace and unchanged repository state |
| Delegation | Independent-agent traces and single-writer integration evidence |
| Missing skills | Bootstrap-only installation with an observed honest fallback |

Use [manual workflow validation](workflow-validation.md) to collect behavioral
evidence. A blocked or unavailable host must be recorded as unrun, not passed.

## Earlier candidate check: 2026-10-20

Source baseline: `b90bfe1`, with the architecture-alignment changes described
above. The changes are prepared as the local 1.1.1 candidate, not a published release.

This historical check predates the live Codex exercise below. Its unrun results
describe that earlier attempt; they do not override the later host-specific evidence.

| Check | Observed result |
|---|---|
| Repository validator | Passed for nine skills, registry, metadata, docs, and fixtures |
| Distribution regression suite | All 10 tests passed; all four package targets exercised |
| Original layout regression | Failed before the fix: direct discovery omitted the five specialists; passed after flattening |
| Bootstrap-only packages | Discovery reference preserved for every target; no extra skills included |
| Candidate Claude startup inventory | All nine namespaced AIEA skills appeared in the startup event |
| Candidate native marketplace/ZIP validation | Attempted; completion not established after automatic approval review stopped the CLI |
| Model-driven repair | Not completed: the CLI returned 401 because its OAuth token had expired |
| Codex and OpenCode inventories | Unrun; CLI startup encountered filesystem access errors |
| Specialist, delegation, and missing-skill behavior | Unrun; no behavioral pass is claimed |

The disposable label example failed its empty/whitespace-input checks as intended
before model invocation. No completed model/tool repair trace was produced, so
that baseline is not evidence of successful self-correction.

Automatic approval review blocked a native Claude check after an attempted
connection to an untrusted Datadog telemetry endpoint. The payload was unknown and
could contain local/project metadata. No attempt was made to bypass that block.
Historical 1.1.0 native-validation results above do not certify this candidate.

## Subsequent live Codex check: 2026-10-20

The [live workflow record](validation/2026-10-20-codex-live-workflow.md) documents
an exercise against 1.1.1 source commit `a26e418`. AIEA skills were explicitly read
through this Codex Work session's tools; automatic activation was not measured.

| Check | Observed result |
|---|---|
| Baseline | Actual failure: empty and whitespace-only labels did not raise ValueError |
| Delegation | Two independent, read-only specialist sessions returned scoped findings |
| Review boundaries | Visible specialist calls were file reads; all four tracked target file hashes and the root file set were unchanged after review |
| Integration | Both reviews finished before the lead edited; only the lead changed the helper |
| Bounded repair | Attempt 1 of a declared budget of 2 produced passing checks |
| Recheck | All three tests passed; tests and requirements remained byte-for-byte unchanged |
| Automatic discovery and other hosts | Not established by this manually loaded Codex run |

This closes the basic repair/delegation smoke check for the observed Codex run.
The follow-up below exercises budget exhaustion. Conflicting reports,
independent-agent failures, missing-skill behavior, and reference-application
behavior remain unverified.

## Triggering, exhaustion, and native-host follow-up: 2026-10-20

The [follow-up record](validation/2026-10-20-triggering-exhaustion-and-hosts.md)
identifies the tested prompts, constraints, commands, and host blockers against
source commit `8d64706`.

| Check | Observed result |
|---|---|
| Exhaustion stop | Worker made exactly two permitted one-behavior repairs, stopped with one failing test, and reported incomplete |
| Independent verification | Lead recheck confirmed the residual failure and unchanged test/requirement hashes; no third fix occurred |
| Claude 2.1.281 structure | Marketplace validation passed; plugin validation passed with the contributor CLAUDE.md warning, with nonessential traffic disabled |
| Claude model run | Blocked by expired OAuth access token, HTTP 401 |
| Native Codex 0.163.0 | Blocked by local access denial during in-process app-server initialization |
| OpenCode 2.0.16 | Started in isolated writable data directories and began model/tool reads; automatic approval review stopped its attempted App Center telemetry connection before completion |
| Automatic triggering | Unverified: no completed native model/tool trace selecting and loading AIEA skills was obtained |

Budget-exhaustion behavior passed only for the explicitly constrained Codex Work
exercise. Native triggering, completed Claude/OpenCode behavior, and broader
reliability are not established by these results.

## Public preview preparation: 2026-10-20

Prepared against `06cf3eb` plus the release-preparation working-tree changes.
Version 1.1.1 was never published separately; it was superseded by the tagged
`v1.2.0`.

| Check | Observed result |
|---|---|
| Repository validator | Passed for all nine skills, metadata, registry, required docs, and fixtures |
| Distribution regression suite | All 11 tests passed locally on Windows with Python 3.11; covers all four ZIPs, license inclusion, hashes, reproducibility, release checksums, and overwrite protection |
| Local release bundle | Four full-skill ZIPs, release notes, and SHA256SUMS generated under `dist/release-1.1.1/` |
| Extracted Claude plugin | Native `claude plugin validate` passed against the newly built, extracted plugin ZIP with nonessential traffic disabled |
| Source manifests | Marketplace validation passed; plugin validation passed with the contributor CLAUDE.md warning, with nonessential traffic disabled |
| CI matrix | Configured for Windows/Linux and Python 3.10/3.12 with downloadable artifacts; hosted runs for these changes have not yet occurred |

Every package now includes the MIT license. Project-skill ZIPs use
`AIEA-LICENSE.txt` to preserve the target project's own `LICENSE`. New
[developer instructions](getting-started.md) provide explicit bootstrap loading,
first-task guidance, and host troubleshooting. The
[release notes](release-notes.md) carry the remaining behavioral limitations.
These distribution checks do not change the native-host results above.

## Codex and OpenCode plugin candidate: 2026-10-20

Version 1.2.0 adds plugin adapters against source baseline `78bd6c7` plus the
working-tree changes. Canonical skill bodies are unchanged from 1.1.1.

| Check | Observed result |
|---|---|
| Offline distribution suite | 15 Python tests passed locally on Windows, Python 3.11.9 and Node 24.14.1; includes all six package targets, subset references, metadata/version alignment, hashes, and release checksums |
| OpenCode adapter contract | Four Node tests imported the actual packaged module and checked nine-skill registration, exact bodies/resource paths, conflicts, unsupported APIs, and missing files using a host API harness |
| Codex installation commands | Syntax checked using local Codex 0.163.0 `plugin ... --help`; no installation into user config was performed |
| Native Codex plugin loading | Unverified; a structurally correct ZIP/local marketplace is not a host-loading pass |
| Native OpenCode 2 adapter loading/model behavior | Unverified; contract tests do not start OpenCode or a model |
| CI matrix | Updated to install Node 22 and exercise all six targets; hosted runs for these changes have not occurred |

The [Codex](../adapters/codex/README.md) and
[OpenCode](../adapters/opencode/README.md) guides distinguish plugins from
project-skill ZIPs. Prior native authentication, filesystem, and telemetry
blockers remain as recorded above; no new automatic-triggering pass is claimed.

## Expanded workflow and specialist candidate: 2026-10-20

The [1.3 exercise record](validation/2026-10-20-skill-expansion.md) describes the
staged expansion to 17 skills: ten core workflows and seven read-only specialist
contracts. It is prepared from the current 1.2 source, based on `abcbaac`.
Main-checkout application is a separate step because its canonical directory is
read-only in this session.

| Check | Observed result |
|---|---|
| Expanded distribution | Validator and all 16 regression tests passed; six host targets and four Node adapter checks covered |
| Claude plugin structure | Native source validation passed with the contributor CLAUDE.md warning; extracted 17-skill plugin passed without warnings, with nonessential traffic disabled |
| Routing | Every registered skill occurs in bootstrap's portable fallback; subset packages retain the fallback resource and missing-skill instructions |
| Manual planning | Guided and baseline runs returned source-backed plans, explicit decisions, and proposed checks; fixtures unchanged |
| Manual testing/browser-QA review | Guided and baseline runs found the redirect/coverage gaps and reported browser checks unrun; fixtures unchanged |
| Implementation/handoff | Each configuration repaired the helper in one of two allowed attempts; lead confirmed passing unchanged tests and only the authorized helper changed |
| Native activation and broader reliability | Unverified; these are manually loaded, bounded examples with no superiority claim |

See the [catalog](skill-catalog.md) and [specialist assignments](specialist-contracts.md)
for the added contracts. The host continues to own agent creation, tools, and
permissions; this expansion does not install independent agents or enforce a sandbox.

## Directory submission preparation: 2026-10-20

Prepared for the Claude Code plugin directory portal. The portal validated the
repository at `main` and reported passing checks with warnings and one policy
hold. The repository changes below address what the portal can check.

| Check | Observed result |
|---|---|
| Claude Code 2.1.281 marketplace validation | `claude plugin validate .` passed with no warnings after the changes below |
| Claude Code 2.1.281 plugin validation | `claude plugin validate .claude-plugin/plugin.json` passed with no warnings; the earlier contributor `CLAUDE.md` warning is gone |
| Listing icon | The plugin folder carries a complete square PNG listing icon at the default location the directory looks for, inside the 512-2048 px and 2 MB limits. No file in the plugin folder names its path, so no script or setting points at an image file. |
| Directory listing metadata | `displayName` is set in `plugin.json`, never in the marketplace entry. The directory-only fields `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`, and `termsOfServiceUrl` are not set: Claude Code ignores them and the directory reports them as unrecognized. `homepage` carries the documentation URL Claude Code does read, and the README carries the documentation, support, and security links the directory shows as the listing description. |
| Registry and packaging | The validator rejects a missing `displayName`, a missing `homepage`, and any directory-only field in the manifest; three regression tests cover the manifest contract and the rename migration. |
| Source-download instructions | `docs/getting-started.md` no longer contains a shell block that fetches code and then executes it, and points at the project page for obtaining the source. |
| Contributor instructions | The root `CLAUDE.md` was removed and its guidance merged into `AGENTS.md`, which Claude Code reads natively; the README states that contributor files are not plugin context |
| Policy hold: name similarity | Resolved. The plugin slug is now `ai-engineering-army`, and the portal reported `Name and publisher checks passed` with no findings. The marketplace maps the former `aiea` name to the new one so existing installs migrate. |
| Policy hold: image reference | Resolved. The listing icon sits at the default location the directory reads, and no file in the plugin folder names its path, so no script or setting points at an image file. |
| Warning: download-and-run pattern | Resolved. The developer guide no longer contains a shell block that fetches code and then executes it. |
| Warning: unrecognized listing fields | Resolved. `documentationUrl` and `supportUrl` are directory-only fields that Claude Code ignores, so they were removed and `homepage` carries the documentation URL instead. The validator now rejects any directory-only field in the manifest. |

Directory review decides what goes live. Native automatic activation of the
skills remains unverified, as recorded above.

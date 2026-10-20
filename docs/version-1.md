# Version 1 scope and acceptance

## Product definition

AIEA 1.x is a usable, portable skill framework for Claude Code, Codex, and OpenCode. It includes canonical skills, deterministic host-layout packaging, repository validation, and the documentation needed to use and maintain the project.

It does not include an orchestration engine, standalone agent, application, online service, automatic installer, or benchmark runner. ArmyBench remains independent.

## Included capabilities

| Area | Version 1 behavior |
|---|---|
| Skill library | Ten core workflows and seven concise read-only specialist contracts in `.agents/skills/`. |
| Activation | Hybrid: native discovery when supported, bootstrap skill for manual discovery. |
| Delegation | Bounded, independent read-only analysis may run in parallel; one active writer integrates changes. |
| Completion | Session-first run ledger, evidence-based checks, bounded repair accounting, and honest scoped reporting. |
| CLI | Dependency-free commands to validate, list, and package the canonical skills. |
| Plugin distribution (1.1) | Claude Code plugin, self-hosted marketplace catalog, and standalone ZIP using the same canonical skills. |
| Plugin adapters (1.2) | Codex compatibility manifest and local-marketplace ZIP; optional OpenCode 2 skill-registration module. The portable skills remain independent. |
| Host support | Claude Code, Codex, and OpenCode project layouts described with official documentation references. |
| Evaluation | Sanitized, illustrative fixture data for later use by separate ArmyBench. |
| Governance | Agent instructions, security guidance, contribution rules, changelog, version, and release procedure. |

## Acceptance criteria

1. All canonical skill directories are direct children of `.agents/skills/`, have valid required metadata and matching names, and occur exactly once in `skill-registry.json` with a valid group.
2. `python tools/aiea.py validate` succeeds from the repository root and checks skill metadata, required v1 documentation, and evaluation fixture JSON.
3. `python tools/aiea.py list` prints all skills and `--group core` or `--group specialists` filters them correctly.
4. `python tools/aiea.py package --host <host>` creates a ZIP with the correct project path for that host, an install note, and a manifest with SHA-256 file hashes.
5. Packaging refuses to overwrite an existing archive and rejects unknown skill names.
6. Packages contain no symlinks and do not include unrelated repository files.
7. CI runs validation and regression checks on Windows/Linux and Python 3.10/3.12 with Node 22 adapter checks, builds all six package targets, and retains downloadable artifacts.
8. The root README and agent instructions state the framework-only boundary and provide copy-pasteable commands.
9. Architecture, host compatibility, CLI, security, contribution, evaluation, and release documentation agree with the implementation.
10. Local validation and packaging require no secrets, network access, or managed runtime. Installing from GitHub requires network access through the host.
11. Plugin metadata matches `VERSION`, explicitly covers every canonical skill once, and resolves within the plugin root.
12. Regression checks cover all six package targets, hashes, selected skills, reproducibility, overwrite protection, and invalid plugin metadata.

13. Bootstrap packages contain a host-neutral discovery reference and explain honest fallback when a selected-skill package omits a needed skill.
14. Every package includes the MIT license without replacing the consumer project's license. The local `release` command prepares all six ZIPs, release notes, and checksums without publishing or overwriting prior output.
15. The Codex plugin ZIP is a self-contained local marketplace. The OpenCode plugin registers only bundled skills, refuses name/ID conflicts, and fails explicitly on unsupported host APIs or missing files. Offline adapter tests are distinguished from native host evidence.
16. Pushing a version tag publishes a GitHub release with every package asset, release notes, and checksums. The release workflow refuses to publish when `VERSION` and the tag disagree, when validation fails, or when the regression suite fails.
17. Every version-bearing file is declared in `.version-bump.json`. One registry drives validation, drift detection, and bumps, and the audit finds version references the registry does not manage.
18. Bootstrap includes a session-first ledger for run/revision identity, working-tree state, host/version, actual skill loads, acceptance checks, assignments, evidence, repair history, blockers, outcome, and next action. File persistence requires authorized scope; secrets and personal data are excluded.
19. Repair defaults are two attempts per stable failure ID and five per run. Explicit user overrides govern. Reserve before corrective changes; interrupted and unverified attempts count, diagnosis and unchanged-code rechecks do not, and multi-failure repairs count for every affected failure and once for the run. Preserve IDs/counters across delegation, reload, handoff, and resume. Unknown prior counts stop repairs; either limit stops further repairs while independent requirements and test expectations remain intact.
20. Every scoped handoff uses exactly one outcome: Failed for a required check confirming a remaining defect; Blocked for an external prerequisite when no confirmed failure takes precedence; Inconclusive for insufficient, stale, flaky, or conflicting evidence; Verified only when all scoped required checks pass at final state. Reports include scope/revision, changes/findings, actual evidence, repair counts/limits, limitations, and next action. Static review is not runtime verification.
21. A repeatable host procedure distinguishes native package loading, explicit activation, fresh-session automatic activation, read-only delegation, successful repair, per-failure and run-wide exhaustion, resumed accounting, missing-skill fallback, and outcome integrity. Evaluate Claude Code, Codex, and OpenCode independently; unavailable checks are blocked or unrun, never inferred as passes. Historical runs and offline adapter tests are not proof for a new candidate.

## Version history

The early v0.1 discussion described the design milestone. The repository adopted
1.0.0 for its initial framework source and 1.1.0 for plugin distribution; those
existing labels are preserved. 1.1.1 records discovery and layout fixes and was
never published separately. The public release 1.2.0, tagged `v1.2.0`, adds
Codex/OpenCode plugin adapters; 1.2.1 adds the tag-triggered release workflow;
1.2.2 adds the declarative version registry; 1.3.0 expanded workflow stages and
specialist contracts to 17 skills. Later unreleased source changes are tracked
in the changelog and do not constitute a published release.
A version bump records a source/API change, not completion of
behavioral evaluation. Changelog dates record source history; hosted release/tag
status is checked separately using the release procedure.

## Operational limits

CI validates the framework structure and package generation. It does not prove that a host installation or agent behavior is correct. Host loading must be smoke-checked manually using each host's current documentation and visible skill inventory. Behavioral evaluation belongs to ArmyBench.

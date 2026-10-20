# Version 1 scope and acceptance

## Product definition

AIEA 1.x is a usable, portable skill framework for Claude Code, Codex, and OpenCode. It includes canonical skills, deterministic host-layout packaging, repository validation, and the documentation needed to use and maintain the project.

It does not include an orchestration engine, standalone agent, application, online service, automatic installer, or benchmark runner. ArmyBench remains independent.

## Included capabilities

| Area | Version 1 behavior |
|---|---|
| Skill library | Four core workflows and five concise read-only specialist contracts in `.agents/skills/`. |
| Activation | Hybrid: native discovery when supported, bootstrap skill for manual discovery. |
| Delegation | Bounded, independent read-only analysis may run in parallel; one active writer integrates changes. |
| Completion | Evidence-based checks and a bounded repair loop with honest reporting. |
| CLI | Dependency-free commands to validate, list, and package the canonical skills. |
| Plugin distribution (1.1) | Claude Code plugin, self-hosted marketplace catalog, and standalone ZIP using the same canonical skills. |
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
7. CI runs validation and regression checks on Windows/Linux and Python 3.10/3.12, builds all four package targets, and retains downloadable artifacts.
8. The root README and agent instructions state the framework-only boundary and provide copy-pasteable commands.
9. Architecture, host compatibility, CLI, security, contribution, evaluation, and release documentation agree with the implementation.
10. Local validation and packaging require no secrets, network access, or managed runtime. Installing from GitHub requires network access through the host.
11. Plugin metadata matches `VERSION`, explicitly covers every canonical skill once, and resolves within the plugin root.
12. Regression checks cover all four package targets, hashes, selected skills, reproducibility, overwrite protection, and invalid plugin metadata.

13. Bootstrap packages contain a host-neutral discovery reference and explain honest fallback when a selected-skill package omits a needed skill.
14. Every package includes the MIT license without replacing the consumer project's license. The local `release` command prepares all four ZIPs, release notes, and checksums without publishing or overwriting prior output.

## Version history

The early v0.1 discussion described the design milestone. The repository adopted
1.0.0 for its initial framework source and 1.1.0 for plugin distribution; those
existing labels are preserved. 1.1.1 is the unreleased patch candidate for discovery
and layout fixes. A version bump records a source/API change, not completion of
behavioral evaluation. Changelog dates record source history; hosted release/tag
status is checked separately using the release procedure.

## Operational limits

CI validates the framework structure and package generation. It does not prove that a host installation or agent behavior is correct. Host loading must be smoke-checked manually using each host's current documentation and visible skill inventory. Behavioral evaluation belongs to ArmyBench.

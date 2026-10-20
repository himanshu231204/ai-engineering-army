# Changelog

All notable AIEA changes are recorded here.

## 1.2.2 - Unreleased

- Added a declarative version registry (`.version-bump.json`) that drives validation, drift detection, and version bumps from one place.
- Added `aiea.py version` with `--check`, `--audit`, and bump modes; bumps rewrite only the version line and stay atomic when a declared file is unreadable.
- Added a repository audit that finds version references outside the registry, and wired it into CI and the release workflow.
- Required the release notes to name the current version, so a release cannot ship stale notes.
- Moved the version out of prose: documentation and adapter guides now use placeholders instead of hardcoded numbers.

## 1.2.1 - 2026-10-20

- Added a tag-triggered release workflow that validates, tests, builds, verifies checksums, and publishes a release with every package asset.
- Added a manual dispatch path with draft and prerelease overrides for releases that need review first.
- Refused to publish when `VERSION` and the release tag disagree.
- Documented the automated release path and kept manual publishing available.

## 1.2.0 - 2026-10-20

- Added a Codex source manifest and self-contained plugin ZIP with a local marketplace.
- Added an optional OpenCode 2 adapter that registers bundled skills without hooks, tools, network access, or orchestration.
- Preserved canonical skill content, standalone project packages, and selected-skill packaging.
- Added adapter metadata checks, offline OpenCode registration/conflict/missing-file tests, and six-target release bundles.
- Documented explicit plugin installation and the distinction between offline adapter tests and native model behavior.

## 1.1.1 - Unreleased (never published; superseded by 1.2.0)

- Prepared a public preview with developer onboarding, explicit activation, and host troubleshooting.
- Included the MIT license in every host package, not only the plugin ZIP.
- Fixed ZIP creator metadata across operating systems for reproducible packaging.
- Added local release bundles with four ZIPs, release notes, and SHA-256 checksums.
- Expanded CI to Windows/Linux and Python 3.10/3.12 with downloadable release artifacts.
- Recorded observed repair/delegation and constrained exhaustion behavior with native-host limitations.
- Flattened all nine canonical skill directories for consistent host discovery.
- Added a validated, host-neutral registry for core/specialist groups.
- Bundled a manual discovery fallback with bootstrap, including missing-skill handling.
- Made verification and bounded repair transitions explicit in bootstrap.
- Added layout/registry regression coverage and manual workflow verification guidance.
- Distinguished source version history from observed behavior and release publication.

## 1.1.0 - 2026-10-20

- Added the `aiea` Claude Code plugin and `aiea-marketplace` self-hosted catalog.
- Registered all nine canonical skills explicitly without maintaining copies.
- Added a standalone `claude-code-plugin` ZIP target with license and hashes.
- Added metadata/version validation, distribution regression tests, and CI coverage.
- Documented local testing, marketplace installation, updates, and release checks.
- Preserved the three existing project-skill package targets and ArmyBench boundary.

## 1.0.0 - 2026-10-20

- Established AIEA as a framework-only portable Agent Skills project.
- Added a dependency-free CLI for validation, listing, and host-layout ZIP packaging.
- Defined host compatibility for Claude Code, Codex, and OpenCode.
- Finalized the v1 architecture, acceptance criteria, security, contribution, and release documentation.
- Preserved the controlled delegation, evidence-based verification, and bounded repair contracts.
- Kept ArmyBench and the Next.js/FastAPI/PostgreSQL application outside the core repository.

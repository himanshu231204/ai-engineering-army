# Changelog

All notable AIEA changes are recorded here.

## 1.1.1 - Unreleased

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

# Changelog

All notable AIEA changes are recorded here.

## 1.4.2 - Unreleased

- Removed the directory-only fields `documentationUrl` and `supportUrl` from the plugin manifest. Claude Code ignores them, and the plugin directory reports them as unrecognized fields.
- Pointed `homepage` at the developer guide, which is the field Claude Code reads as the documentation URL.
- Added validation that rejects directory-only fields in the manifest, and surfaced documentation and support links in the README, which the directory uses as the listing description.

## 1.4.1 - Unreleased

- Rewrote the source-build instructions in the developer guide so no shell block fetches and then executes code, and pointed at the project page for obtaining the source.

## 1.4.0 - Unreleased

- Renamed the plugin from `aiea` to `ai-engineering-army` so the directory listing cannot be confused with existing short connector names. The marketplace maps the former name to the new one, so existing installs migrate instead of failing.
- Moved the listing icon to the default location the directory looks for and removed every file reference to its path, so no script or setting points at an image file.
- Added the directory listing fields `displayName`, `documentationUrl`, and `supportUrl`.

## 1.3.3 - Unreleased

- Added a listing icon for the plugin directory, plus the directory listing fields `displayName`, `documentationUrl`, and `supportUrl`.
- Added validation that rejects a missing, non-square, out-of-range, oversized, or wrong-format listing icon, and a missing `displayName`.
- Shipped the listing icon inside the Claude Code plugin ZIP.
- Split the source-download instructions into a fetch step that runs nothing and a separate build step that asks the reader to review the files first.
- Removed the root `CLAUDE.md` and merged its guidance into `AGENTS.md`, which Claude Code reads natively, clearing the plugin validator warning.
- Documented what the plugin runs, sends, and fetches in the README.

## 1.3.2 - Unreleased

- Published every tagged version as a full public release instead of a prerelease, so the Releases section lists them without prerelease badges.
- Changed the release workflow to publish full releases on a tag push; the `prerelease` input remains available for candidates that need one.

## 1.3.1 - 2026-10-20

- Added GitHub issue templates for bug reports, evidence-backed reports, feature requests, and new host support, with blank issues disabled and questions routed to Discussions.
- Added a pull request template that requires the submitting model and host, the problem, the scope check, alternatives considered, the commands run with their exit codes, and a human review of the complete diff.
- Required the issue and pull request templates as repository documents so validation fails if one goes missing.

## 1.3.0 - 2026-10-20

- Expanded to ten core workflows with reconnaissance, requirements discovery, architecture design, task planning, implementation, and handoff.
- Added testing and browser-QA specialists, bringing read-only specialist contracts to seven roles.
- Extended discovery, Claude registration, and all host packages to 17 skills while preserving existing identifiers.
- Documented specialist capabilities, permissions, evidence, failure escalation, and lead-only integration.
- Added expanded-inventory/routing coverage and illustrative manual exercise prompts; native activation remains unverified.

## 1.2.2 - 2026-10-20

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

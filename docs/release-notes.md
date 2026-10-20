# AIEA 1.2.0 public preview

AIEA is an MIT-licensed portable engineering skill library for Claude Code, Codex,
and OpenCode. This preview contains nine skills, plugin adapters for all three
hosts, and dependency-free distribution tools. It adds no orchestration runtime,
automatic installer, hooks, telemetry, or benchmark runner.

## Changes

- All nine skills now use a flat discovery layout and a validated core/specialist registry.
- Bootstrap includes a portable discovery reference and reports missing skills honestly.
- Explicit verification and bounded repair guidance connects the workflow stages.
- Every host ZIP includes the MIT license, installation notes, and per-file hashes.
- ZIP creator metadata is fixed across operating systems, alongside fixed timestamps.
- Codex has a source manifest and a self-contained local-marketplace plugin ZIP.
- OpenCode 2 has a dependency-free JavaScript adapter that registers bundled skills and refuses conflicting names.
- A local release command prepares six ZIPs, these notes, and `SHA256SUMS`.
- A developer guide covers installation, first use, explicit loading, and troubleshooting.

## Choose an asset

| Asset suffix | Use |
|---|---|
| `claude-code-plugin.zip` | Extract separately; load with `claude --plugin-dir /path/to/extracted-plugin`. |
| `claude-code.zip` | Extract into a target project for `.claude/skills/` project skills. |
| `codex.zip` | Extract into a target project for `.agents/skills/`. |
| `opencode.zip` | Extract into a target project for `.agents/skills/`. |
| `codex-plugin.zip` | Extract separately; add the directory with `codex plugin marketplace add`, then install `aiea@aiea-marketplace`. |
| `opencode-plugin.zip` | Extract separately; add the directory to OpenCode 2's `plugins` config. |

Compare the archive's SHA-256 with `SHA256SUMS` before extraction. Review existing
skill-name conflicts. Installed skills need no Python; source packaging requires
Python 3.10+. A working coding host and its model access are required.

[Developer quick start](https://github.com/himanshu231204/ai-engineering-army/blob/main/docs/getting-started.md)
includes the marketplace commands. Marketplace installation tracks the default
branch; these release assets are the versioned alternative.

## Evidence and limits

Offline regression checks cover layout, metadata, all six packages, license
inclusion, hashes, subsets, reproducibility, and overwrite protection. CI runs
these checks; review the result for the source commit being published.

The packaged OpenCode adapter has offline setup tests for registration, skill-name
conflicts, missing files, and unsupported host APIs. Its only runtime behavior is
reading bundled files and contributing skill definitions. Native Codex plugin
installation and OpenCode 2 plugin loading/model invocation remain unverified.
Use either the plugin or the project skills per host/project to avoid duplicates.

Observed Codex Work exercises with manually loaded skills demonstrated read-only
delegation, one-writer repair, and stopping at an explicitly constrained repair
budget. Claude manifests passed native validation. These observations are bounded
smoke checks, not broad reliability measurements.

Automatic activation and completed native Claude/OpenCode model workflows remain
unverified. Claude model execution encountered expired authentication; native
Codex startup encountered OS access denial; an OpenCode run was interrupted by
environment approval review of a host telemetry request. These were host/environment
blockers, not established AIEA defects. AIEA itself includes no telemetry.

Invoke bootstrap explicitly and check actual loading evidence. Specialist skills
are instructions, not installed agent processes, and read-only boundaries and
repair budgets depend on host/model compliance. See the
[verification record](https://github.com/himanshu231204/ai-engineering-army/blob/main/docs/verification-status.md).

This file describes the `v1.2.0` public preview. Building the bundle locally does
not publish a GitHub release or certify additional behavioral checks.

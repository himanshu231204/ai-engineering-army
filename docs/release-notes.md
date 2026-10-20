# AIEA 1.1.1 public preview

AIEA is an MIT-licensed portable engineering skill library for Claude Code, Codex,
and OpenCode. This preview contains nine skills, a Claude Code marketplace/plugin
adapter, and dependency-free distribution tools. It adds no orchestration runtime,
automatic installer, hooks, telemetry, or benchmark runner.

## Changes

- All nine skills now use a flat discovery layout and a validated core/specialist registry.
- Bootstrap includes a portable discovery reference and reports missing skills honestly.
- Explicit verification and bounded repair guidance connects the workflow stages.
- Every host ZIP includes the MIT license, installation notes, and per-file hashes.
- ZIP creator metadata is fixed across operating systems, alongside fixed timestamps.
- A local release command prepares four ZIPs, these notes, and `SHA256SUMS`.
- A developer guide covers installation, first use, explicit loading, and troubleshooting.

## Choose an asset

| Asset suffix | Use |
|---|---|
| `claude-code-plugin.zip` | Extract separately; load with `claude --plugin-dir /path/to/extracted-plugin`. |
| `claude-code.zip` | Extract into a target project for `.claude/skills/` project skills. |
| `codex.zip` | Extract into a target project for `.agents/skills/`. |
| `opencode.zip` | Extract into a target project for `.agents/skills/`. |

Compare the archive's SHA-256 with `SHA256SUMS` before extraction. Review existing
skill-name conflicts. Installed skills need no Python; source packaging requires
Python 3.10+. A working coding host and its model access are required.

[Developer quick start](https://github.com/himanshu231204/ai-engineering-army/blob/main/docs/getting-started.md)
includes the marketplace commands. Marketplace installation tracks the default
branch; these release assets are the versioned alternative.

## Evidence and limits

Offline regression checks cover layout, metadata, all four packages, license
inclusion, hashes, subsets, reproducibility, and overwrite protection. CI runs
these checks; review the result for the source commit being published.

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

This file describes a release candidate. Preparing it locally does not publish a
GitHub release or certify additional behavioral checks.

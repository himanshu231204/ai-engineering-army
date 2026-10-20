# AI Engineering Army (AIEA)

AIEA is an open-source, portable Agent Skills framework for Claude Code, Codex, and OpenCode. It improves engineering workflows in the coding host people already use. It is not a standalone coding agent, orchestration engine, or application.

**Current release:** [latest GitHub release](https://github.com/himanshu231204/ai-engineering-army/releases) · **License:** MIT

Start with the [developer guide](docs/getting-started.md) for installation,
your first task, and troubleshooting. Use explicit bootstrap activation for the
preview. Packaging and bounded Codex Work exercises have been checked; automatic
activation and completed native Claude/OpenCode model workflows remain unverified.
See [the evidence and limits](docs/verification-status.md).

## What v1 includes

- A Claude Code marketplace/plugin adapter and standalone plugin ZIP.
- A Codex plugin/local-marketplace ZIP and an optional OpenCode 2 skill-registration plugin.
- Nine portable skills: four core workflow skills and five read-only specialist contracts.
- A dependency-free Python CLI to validate and list skills and build ZIP packages for supported hosts.
- Host compatibility guidance for native discovery and packaged skill locations.
- Security, contribution, release, evaluation, and final architecture documentation.
- A small evaluation fixture for the separate ArmyBench project.

## Claude Code plugin

AIEA includes a Claude Code plugin and its own marketplace. The following commands
install the version currently available on the repository default branch:

```text
/plugin marketplace add himanshu231204/ai-engineering-army
/plugin install aiea@aiea-marketplace
```

Start with `/aiea:aiea-bootstrap`. To try a local checkout, use
`claude --plugin-dir /path/to/ai-engineering-army` from a separate target project.
See [plugin installation, all nine commands, and smoke checks](docs/claude-code-plugin.md).
No Python is needed to use the installed plugin; Python is for maintainer tooling.

## Codex and OpenCode plugins

Build the matching adapter from this checkout:

```sh
python tools/aiea.py package --host codex-plugin
python tools/aiea.py package --host opencode-plugin
```

Extract each ZIP into its own directory. For Codex, add the extracted local
marketplace and install `aiea@aiea-marketplace`. For OpenCode 2, add the extracted
directory to your project's `plugins` configuration. Follow the exact commands
in the [Codex adapter](adapters/codex/README.md) or
[OpenCode adapter](adapters/opencode/README.md). Keep either plugin or project
skills enabled per host/project to avoid duplicates. Native installation and
model-driven use of these new adapters remain unverified.

## Quick start

Requires Python 3.10 or later. The CLI uses only the Python standard library.

```sh
python tools/aiea.py --version
python tools/aiea.py validate
python tools/aiea.py list
python tools/aiea.py list --group core
python tools/aiea.py version --check
```

Build a package for a target project:

```sh
python tools/aiea.py package --host claude-code
python tools/aiea.py package --host codex
python tools/aiea.py package --host opencode
```

Archives are written to `dist/` and contain the host's skill path. Extract the archive at the target project's root after reviewing the package and checking for existing skill-name conflicts. To select only specific skills, repeat `--skill`:

```sh
python tools/aiea.py package --host claude-code --skill aiea-bootstrap --skill security-review
```

Codex and OpenCode can also discover the canonical `.agents/skills/` directory directly when the repository itself is the target project. Claude Code project skills use `.claude/skills/`; the CLI produces that layout for Claude Code.

See [CLI usage](docs/cli.md), [host compatibility](docs/host-compatibility.md), and the [v1 definition of done](docs/version-1.md).

Prebuilt archives for every host are attached to each
[GitHub release](https://github.com/himanshu231204/ai-engineering-army/releases),
along with `SHA256SUMS` for verification.

Maintainers can prepare all six packages, release notes, and checksums locally:

```sh
python tools/aiea.py release
```

The bundle is written to `dist/release-<VERSION>/`. This command does not publish.
See [the release procedure](docs/release.md).

See [verification status](docs/verification-status.md) for observed host checks and
[manual workflow validation](docs/workflow-validation.md) for the repair/delegation checklist.

## Project principles

- **Portable skills first:** canonical sources live in `.agents/skills/` and use the [Agent Skills format](https://agentskills.io/specification).
- **Hybrid activation:** use a host's native discovery where available; bootstrap guidance helps when activation is manual or inconsistent.
- **Controlled delegation:** independent read-only specialists may analyze in parallel; one lead integrates changes as the sole active writer.
- **Evidence-based completion:** report checks and results, and keep repairs bounded.
- **Least privilege:** skills provide instructions; they do not grant tools, credentials, or permissions.
- **Optional runtime later:** managed coordination may be considered separately without making skills depend on it.

## Repository map

- `.agents/skills/` — canonical core skills and specialist contracts.
- `skill-registry.json` - portable skill names and core/specialist groups.
- `.version-bump.json` - every file that carries the repository version.
- `.claude-plugin/` — Claude Code plugin manifest and marketplace catalog.
- `.codex-plugin/` - Codex plugin source manifest.
- `tools/aiea.py` — validation, listing, and host package CLI.
- `adapters/` — host discovery and packaging guidance; see verification status for observed checks.
- `evaluations/fixtures/` — small, host-neutral examples.
- `docs/` — vision, final architecture, v1 acceptance, security, contribution, CLI, host, and release guidance.
- `AGENTS.md` and `CLAUDE.md` — shared coding-agent instructions.

ArmyBench is a separate project. This repository does not contain its application, runner, scoring service, or benchmark dataset. The initial evaluation stack is Next.js, FastAPI, and PostgreSQL.

## Development checks

```sh
python tools/aiea.py validate
python -m unittest discover -s tests -v
python tools/aiea.py package --host claude-code-plugin --output .tmp/packages
python tools/aiea.py package --host claude-code --output .tmp/packages
python tools/aiea.py package --host codex --output .tmp/packages
python tools/aiea.py package --host opencode --output .tmp/packages
python tools/aiea.py package --host codex-plugin --output .tmp/packages
python tools/aiea.py package --host opencode-plugin --output .tmp/packages
```

The package command refuses to overwrite an existing archive. Remove or choose a different output directory before rebuilding the same host package. See [contribution rules](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

## Sponsor

AIEA is free and MIT-licensed, and it stays that way. Sponsorship pays for the
maintainer time behind host verification runs, releases, and documentation — not
for a paid tier, a hosted service, or telemetry.

Sponsor the project on [GitHub Sponsors](https://github.com/sponsors/himanshu231204).

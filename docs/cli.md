# AIEA CLI

The CLI is a standard-library Python script. It runs from a checkout and requires Python 3.10 or later. It does not install itself globally.

## Commands

```sh
python tools/aiea.py --version
python tools/aiea.py validate
python tools/aiea.py list
python tools/aiea.py list --group core
python tools/aiea.py list --group specialists
```

Build a host-layout archive:

```sh
python tools/aiea.py package --host claude-code
python tools/aiea.py package --host codex --output .tmp/packages
python tools/aiea.py package --host opencode --skill aiea-bootstrap --skill security-review
```

`--host` is required and must be `claude-code`, `codex`, or `opencode`. `--output` chooses the directory for the ZIP archive and defaults to `dist/`. Repeat `--skill` to include a selected set; without it, all skills are included.

## Validation

`validate` checks:

- `SKILL.md` frontmatter delimiters, required `name` and `description`, Agent Skills name and description limits, name-to-directory agreement, duplicate names, and symlinks;
- `VERSION` semantic version format;
- required v1 documentation;
- JSON syntax for evaluation fixtures.

This is a focused structural check, not a complete YAML implementation or a behavioral evaluator. CI also builds each host archive to ensure the package paths and manifest generation work.

## Package contents

A package ZIP contains only selected skill directories under the host-specific project path, `AIEA-INSTALL.md`, and `aiea-manifest.json`. The manifest records version, host, install path, skill names, file sizes, and SHA-256 digests. Archive timestamps are fixed to keep repeated builds reproducible.

The CLI refuses to overwrite an existing archive. Choose a new output directory or remove the old archive deliberately before rebuilding. The CLI never extracts packages into another project or changes host configuration.

## Exit behavior

- `0`: command completed successfully.
- `1`: validation or filesystem error.
- `2`: invalid command selection, unknown skill, or existing output archive.

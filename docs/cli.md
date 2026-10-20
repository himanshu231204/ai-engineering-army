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

`--host` is required and must be `claude-code`, `claude-code-plugin`, `codex`, or `opencode`. `--output` chooses the directory for the ZIP archive and defaults to `dist/`. Repeat `--skill` to include a selected set; without it, all skills are included.

## Validation

`validate` checks:

- direct skill-directory layout and exact name/group membership in `skill-registry.json`;
- `SKILL.md` frontmatter delimiters, required `name` and `description`, Agent Skills name and description limits, name-to-directory agreement, duplicate names, and symlinks;
- `VERSION` semantic version format;
- plugin and marketplace JSON, matching release versions, and complete canonical skill registration;
- required v1 documentation;
- JSON syntax for evaluation fixtures.

This is a focused structural check, not a complete YAML implementation or a behavioral evaluator. Run `python -m unittest discover -s tests -v` for offline regression checks. CI also builds each host archive to ensure the package paths and manifest generation work.

Skill grouping comes from `skill-registry.json`, not directory nesting. The
registry is maintenance metadata and does not need to be installed in a target
project. Bootstrap carries its own discovery reference with every package.

## Package contents

Project-skill ZIPs contain selected skill directories under the host-specific
project path, `AIEA-LICENSE.txt`, `AIEA-INSTALL.md`, and `aiea-manifest.json`. The separate license name avoids replacing the target project's `LICENSE`. The `claude-code-plugin`
target instead places skills under `skills/` and also includes a generated
`.claude-plugin/plugin.json` and `LICENSE`. Load its extracted directory with
`claude --plugin-dir`; do not extract it as project skills. See the
[plugin guide](claude-code-plugin.md). The manifest records version, host, install path, skill names, file sizes, and SHA-256 digests. Archive timestamps are fixed to keep repeated builds reproducible.

The CLI refuses to overwrite an existing archive. Choose a new output directory or remove the old archive deliberately before rebuilding. The CLI never extracts packages into another project or changes host configuration.

## Prepare a release bundle

```sh
python tools/aiea.py release
python tools/aiea.py release --output .tmp/release-review
```

`release` validates the repository and stages all four full-skill ZIPs,
`RELEASE-NOTES.md` from `docs/release-notes.md`, and `SHA256SUMS`. The default
destination is `dist/release-<VERSION>/`. It refuses any existing destination,
including an empty directory. ZIP timestamps and creator metadata are fixed.
Repeated builds with unchanged source bytes and the same Python/compression
toolchain produce identical ZIPs and checksums; checkout line endings or
compression-library changes can affect bytes across environments.
No network, credentials, Git writes, publishing, or host execution
is involved. Run the regression suite separately before publishing.

If a filesystem error interrupts final copying, output may be partial. Do not
publish that directory; inspect it and choose a fresh destination for a retry.
Checksums cover all four ZIPs and the notes, not `SHA256SUMS` itself. Checksums
are not signatures or proof of publisher identity.

## Exit behavior

- `0`: command completed successfully.
- `1`: validation or filesystem error.
- `2`: invalid command selection, unknown skill, or existing output archive.

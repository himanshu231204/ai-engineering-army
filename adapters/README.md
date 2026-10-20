# Host adapters

The canonical source is `.agents/skills/`. The v1 CLI builds ZIP archives that place those skills under a supported host's project-level skill directory. Adapter notes document the exact path and discovery behavior; the portable skill content is not duplicated in this repository.

Claude Code additionally supports a marketplace plugin and a standalone plugin ZIP.
Version 1.2 adds a Codex plugin/local-marketplace ZIP and an OpenCode 2 plugin
that contributes skill definitions. All adapters package the same canonical
source; the OpenCode adapter is optional JavaScript registration code with no
hooks, tools, network calls, or orchestration.

- [Claude Code](claude-code/README.md)
- [Codex](codex/README.md)
- [OpenCode](opencode/README.md)

Host behavior changes. Check the linked official docs in each adapter before changing a path or publishing a package.

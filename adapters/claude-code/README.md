# Claude Code adapter

## Marketplace plugin (1.1)

The `aiea` plugin and `aiea-marketplace` catalog live in `.claude-plugin/` at the
repository root. The plugin references every canonical skill directory directly,
including specialists, without duplicating portable content. Plugin commands
use the `ai-engineering-army:` namespace. See [installation and smoke checks](../../docs/claude-code-plugin.md).

For a standalone plugin distribution:

```sh
python tools/aiea.py package --host claude-code-plugin
```

## Project skills

Claude Code project skills use `.claude/skills/<name>/SKILL.md`. The canonical AIEA sources stay under `.agents/skills/`; build a package with:

```sh
python tools/aiea.py package --host claude-code
```

Extract the archive at the target project's root after reviewing it and checking for duplicate skill names. The package contains portable Agent Skills content and does not configure Claude Code permissions, plugins, or user-level settings.

Official reference: [Claude Code skills](https://code.claude.com/docs/en/skills).

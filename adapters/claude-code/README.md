# Claude Code adapter

Claude Code project skills use `.claude/skills/<name>/SKILL.md`. The canonical AIEA sources stay under `.agents/skills/`; build a package with:

```sh
python tools/aiea.py package --host claude-code
```

Extract the archive at the target project's root after reviewing it and checking for duplicate skill names. The package contains portable Agent Skills content and does not configure Claude Code permissions, plugins, or user-level settings.

Official reference: [Claude Code skills](https://code.claude.com/docs/en/skills).

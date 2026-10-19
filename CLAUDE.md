# Claude Code instructions

@AGENTS.md

## Skill discovery in this repository

The canonical AIEA skills live in `.agents/skills/`. Do not assume Claude Code loaded them from that directory. When this repo's workflow is relevant, read the matching canonical `SKILL.md` directly. For a consumer project, `python tools/aiea.py package --host claude-code` creates a package under `.claude/skills/`.

Never edit generated package copies as source. Change `.agents/skills/` and rebuild the package. Before changing host packaging behavior, check the official Claude Code documentation and update `adapters/claude-code/README.md` and `docs/host-compatibility.md`.

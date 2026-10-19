# Host compatibility

AIEA targets project-local skills in Claude Code, Codex, and OpenCode. The portable skill contents remain canonical under `.agents/skills/`; the CLI writes an archive containing the appropriate path for the selected host.

| Host | Project skill path in package | Native path notes |
|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md` | Claude Code project skills are discovered from `.claude/skills/`. |
| Codex | `.agents/skills/<name>/SKILL.md` | Codex discovers repository skills from `.agents/skills/`. |
| OpenCode | `.agents/skills/<name>/SKILL.md` | OpenCode supports `.agents/skills/` and its native `.opencode/skills/`; AIEA uses the shared path to avoid duplicate sources. |

## Use the canonical tree

If the target is this repository, Codex and OpenCode can discover `.agents/skills/` natively. Claude Code uses the generated Claude package path.

For another project, generate a package and extract it at that project's root after reviewing the archive and checking for skill-name conflicts:

```sh
python tools/aiea.py package --host claude-code
python tools/aiea.py package --host codex
python tools/aiea.py package --host opencode
```

Packages are project-local. Global installation paths, host configuration, permissions, plugins, marketplaces, and user-level setup are outside v1. AIEA does not modify those locations.

## Official references

Host discovery behavior changes over time. These references were checked for v1 on 2026-10-20; verify them again before changing packaging:

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skills](https://developers.openai.com/codex/skills)
- [OpenCode skills](https://opencode.ai/docs/skills)

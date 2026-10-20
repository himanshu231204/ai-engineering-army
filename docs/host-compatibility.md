# Host compatibility

AIEA targets project-local skills in Claude Code, Codex, and OpenCode. The portable skill contents remain canonical under `.agents/skills/`; the CLI writes an archive containing the appropriate path for the selected host.

| Host | Project skill path in package | Native path notes |
|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md` | Claude Code project skills are discovered from `.claude/skills/`. |
| Codex | `.agents/skills/<name>/SKILL.md` | Codex discovers repository skills from `.agents/skills/`. |
| OpenCode | `.agents/skills/<name>/SKILL.md` | OpenCode supports `.agents/skills/` and its native `.opencode/skills/`; AIEA uses the shared path to avoid duplicate sources. |

## Claude Code plugin distribution

Version 1.1 additionally supports `aiea@aiea-marketplace`. The source manifest
explicitly registers each canonical skill, including all five specialists. In 1.1.1 all canonical skills are direct children of `.agents/skills/` so the source layout also matches project discovery. The
`claude-code-plugin` package target uses `.claude-plugin/plugin.json` and
`skills/<name>/SKILL.md`. This differs from the project-skill ZIP in the table.
See [installation and verification](claude-code-plugin.md).

## Codex and OpenCode plugin distribution (1.2)

| Target | Plugin layout | Activation |
|---|---|---|
| `codex-plugin` | `.codex-plugin/plugin.json`, `skills/`, local `.agents/plugins/marketplace.json` | Add the extracted local marketplace, install `aiea@aiea-marketplace`, and request bootstrap in a new session. |
| `opencode-plugin` | `package.json`, `index.js`, `skills-index.json`, `skills/` | Add the extracted directory to OpenCode 2's `plugins` configuration; the adapter contributes skill definitions. |

These ZIPs are extracted into separate directories, not into a target project.
Use either the plugin or project skills to avoid duplicate names. The OpenCode
adapter is optional local registration code; canonical instructions still work
without it. It has no event hooks, tools, network calls, or permissions of its
own. Its contract tests do not certify native host loading or model invocation.
See the [Codex](../adapters/codex/README.md) and
[OpenCode](../adapters/opencode/README.md) guides for installation and limits.

## Use the canonical tree

If the target is this repository, Codex and OpenCode can discover `.agents/skills/` natively. Claude Code uses the generated Claude package path.

For another project, generate a package and extract it at that project's root after reviewing the archive and checking for skill-name conflicts:

```sh
python tools/aiea.py package --host claude-code
python tools/aiea.py package --host codex
python tools/aiea.py package --host opencode
```

Project-skill packages are project-local. The ZIP commands do not manage global paths, host settings, or permissions. Plugin installation is explicitly performed through the chosen host, using the adapter instructions. AIEA's packaging CLI does not modify those locations.

## Verification limits

The directory layouts above follow the official references. A matching layout is
structural evidence; it does not establish that a particular host session loaded
the skills. Record the actual inventory and host version using
[verification status](verification-status.md).

## Official references

Host discovery behavior changes over time. These references were checked for v1 on 2026-10-20; verify them again before changing packaging:

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skills](https://developers.openai.com/codex/skills)
- [OpenCode skills](https://opencode.ai/docs/skills)
- [Codex plugins and marketplace schema](https://developers.openai.com/plugins/build/plugins)
- [OpenCode 2 plugin API](https://opencode.ai/v2/docs/build/plugins)

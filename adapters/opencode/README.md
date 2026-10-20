# OpenCode adapter

## Optional OpenCode 2 plugin (1.2)

Build the local adapter:

```sh
python tools/aiea.py package --host opencode-plugin
```

Extract `dist/aiea-1.2.0-opencode-plugin.zip` into a separate directory. In your
target project's `opencode.json` or `opencode.jsonc`, merge the following entry
with existing configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["/absolute/path/to/extracted-aiea"]
}
```

On Windows, use a JSON path such as `C:/tools/aiea-opencode`. Preserve other
plugin entries and restart OpenCode. Ask it to load `aiea-bootstrap` and state
your task and acceptance checks. Do not point at the source
`adapters/opencode/plugin/` folder: the generated ZIP adds the skill index and
bundled skills required by the entrypoint.

The adapter targets the OpenCode 2 `id`/`setup` plugin contract and
`ctx.skill.transform` API. It reads only its bundled index and skill files, then
registers names, descriptions, absolute resource paths, and skill bodies. Names
remain the canonical names; registry IDs use `aiea:<skill-name>`. Eligible skills
can be selected by the host (`autoinvoke: true`); registration does not prove that
the host selected a skill or that the model followed it.

The plain JavaScript adapter has no npm dependencies, network calls, tools,
event hooks, permission changes, config writes, or session-injection behavior.
It does not add a coordinator or enforce repair budgets. It refuses name/ID
conflicts instead of replacing another skill. Choose either this plugin or
project-skill installation for a target project. To remove it, remove only its
entry from your `plugins` list and restart before removing the extracted files.

Older OpenCode versions should use the portable package below. The adapter is
tested offline with a contract harness, not a completed native OpenCode model
session. Prior host telemetry restrictions remain unresolved; see
[verification status](../../docs/verification-status.md).

## Portable project skills

OpenCode discovers project skills under `.agents/skills/` and also has its own `.opencode/skills/` path. AIEA packages to the shared `.agents/skills/` path so one source tree works across Codex and OpenCode:

```sh
python tools/aiea.py package --host opencode
```

Extract the archive at the target project root after reviewing it and checking for duplicate skill names. The package does not edit `opencode.json`, set skill permissions, or install globally.

Official reference: [OpenCode skills](https://opencode.ai/docs/skills).

Plugin references: [OpenCode 2 plugin API](https://opencode.ai/v2/docs/build/plugins)
and [Skill.Info schema](https://opencode.ai/v2/docs/api#skillinfo).

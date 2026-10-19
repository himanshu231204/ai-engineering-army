# OpenCode adapter

OpenCode discovers project skills under `.agents/skills/` and also has its own `.opencode/skills/` path. AIEA packages to the shared `.agents/skills/` path so one source tree works across Codex and OpenCode:

```sh
python tools/aiea.py package --host opencode
```

Extract the archive at the target project root after reviewing it and checking for duplicate skill names. The package does not edit `opencode.json`, set skill permissions, or install globally.

Official reference: [OpenCode skills](https://opencode.ai/docs/skills).

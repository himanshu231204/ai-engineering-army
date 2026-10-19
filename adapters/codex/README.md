# Codex adapter

Codex discovers project skills under `.agents/skills/`, which is also AIEA's canonical source location. In this repository, no copy is needed. For another project, create a host-layout archive with:

```sh
python tools/aiea.py package --host codex
```

Extract the archive at the target project root after reviewing it and checking for duplicate skill names. The package does not change Codex configuration, permissions, or personal skills.

Official reference: [Codex skills](https://developers.openai.com/codex/skills).

# Codex adapter

## Installable plugin (1.2)

Build a self-contained local marketplace from the AIEA checkout:

```sh
python tools/aiea.py package --host codex-plugin
```

Extract `dist/aiea-1.2.1-codex-plugin.zip` into a separate directory, keeping
hidden folders. It includes `.codex-plugin/plugin.json`, the nine skills under
`skills/`, and `.agents/plugins/marketplace.json`. From your terminal, run:

```sh
codex plugin marketplace add /absolute/path/to/extracted-aiea
codex plugin add aiea@aiea-marketplace
```

Use the extracted directory's actual path. These host commands change your Codex
plugin configuration. Inspect any existing marketplace named `aiea-marketplace`
before adding a different source under that name. Keep the extracted directory
available while the host tracks it. Open a new session in your target project
and ask Codex to load `aiea-bootstrap`, then provide your engineering task.
If your client has no `plugin add` command, use its plugin UI after adding the
marketplace, or use project skills below.

The source `.codex-plugin/plugin.json` points at the canonical `.agents/skills/`.
The packaged manifest is rewritten to `./skills/`; no source copies are maintained.
The ZIP supplies its own Codex marketplace. This repo's Claude marketplace command
is not the Codex installation command, and no public OpenAI directory listing or
remote Codex marketplace installation is claimed.

Use either project skills or the plugin in a target project to avoid duplicate
names. To uninstall, run `codex plugin remove aiea@aiea-marketplace`; inspect
`codex plugin remove --help` for your installed client. Remove the marketplace
only if no other installation uses it.

## Portable project skills

Codex discovers project skills under `.agents/skills/`, which is also AIEA's canonical source location. In this repository, no copy is needed. For another project, create a host-layout archive with:

```sh
python tools/aiea.py package --host codex
```

Extract the archive at the target project root after reviewing it and checking for duplicate skill names. The package does not change Codex configuration, permissions, or personal skills.

Official reference: [Codex skills](https://developers.openai.com/codex/skills).

Plugin references: [packaging and marketplace schema](https://developers.openai.com/plugins/build/plugins).
Command syntax was checked with local Codex CLI 0.163.0 help. Native plugin
installation and model-driven invocation remain unverified; the offline tests
verify package metadata, local paths, hashes, and skill contents.

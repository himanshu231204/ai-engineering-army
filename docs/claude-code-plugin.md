# AIEA for Claude Code

AIEA 1.1 adds a Claude Code plugin named `aiea` and a self-hosted marketplace
named `aiea-marketplace`. The plugin exposes the same nine canonical skills as
the portable framework. It adds no hooks, background services, MCP servers,
credentials, or permission changes. Specialist skills remain read-only guidance;
installing them does not create autonomous subagent processes.

## Try this checkout

From the repository root, validate the manifests:

```sh
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

Start Claude Code from a separate target project with the checkout as the plugin:

```sh
claude --plugin-dir /path/to/ai-engineering-army
```

Replace that example path with your actual checkout. Inside Claude Code, run:

```text
/aiea:aiea-bootstrap
```

For a complete local marketplace installation, run these shell commands from
the AIEA checkout:

```sh
claude plugin marketplace add .
claude plugin install aiea@aiea-marketplace --scope user
claude plugin list
claude plugin details aiea
```

These installation commands change the selected Claude Code configuration.
Use a separate `CLAUDE_CONFIG_DIR` for disposable installation tests. Start a new
session after installing, or run `/reload-plugins` in an existing session.

## Install from GitHub after publication

These commands require the marketplace files to be pushed to the repository's
default branch. They will not install an unpublished local change.

```text
/plugin marketplace add himanshu231204/ai-engineering-army
/plugin install aiea@aiea-marketplace
```

Review the installation scope in the plugin panel. After activating the plugin,
run `/aiea:aiea-bootstrap` with your engineering task. Claude can also select a
relevant skill by its description; automatic selection is model behavior, not a
guarantee that every workflow runs on every task.

This is AIEA's own marketplace. Inclusion in Anthropic's public directory requires
a separate submission; this repository does not claim that approval.

## Skill inventory

| Invocation | Purpose |
|---|---|
| `/aiea:aiea-bootstrap` | Discover relevant skills and establish the task workflow |
| `/aiea:controlled-delegation` | Scope independent reviews and keep one active writer |
| `/aiea:evidence-verification` | Select checks and report observed results |
| `/aiea:bounded-repair` | Diagnose and repair within an explicit attempt budget |
| `/aiea:architecture-review` | Review boundaries, coupling, and data flow |
| `/aiea:backend-review` | Review API and service behavior |
| `/aiea:data-review` | Review data models, migrations, and integrity |
| `/aiea:frontend-review` | Review UI behavior, accessibility, and state |
| `/aiea:security-review` | Review authorization, inputs, secrets, and trust boundaries |

## Source and standalone ZIP layouts

The repository is both marketplace root and plugin root (`source: "./"`).
`.claude-plugin/plugin.json` explicitly lists each canonical skill directory,
including all five specialists. Version 1.1.1 makes every canonical skill a direct
child of `.agents/skills/`; core/specialist groups live in `skill-registry.json`. All referenced files are inside the plugin root,
so copying the repository into Claude Code's plugin cache preserves them. There
are no symlinks or maintained skill copies.

Build a standalone plugin ZIP with:

```sh
python tools/aiea.py package --host claude-code-plugin
```

Extract it into a separate directory. It contains `.claude-plugin/plugin.json`,
the selected skills under `skills/<name>/SKILL.md`, the MIT license, installation
notes, and a hash manifest. Its generated plugin manifest uses the default
`skills/` layout and has no references back to this checkout. Load the extracted
directory with `claude --plugin-dir /path/to/extracted-plugin`.

`--skill` supports a deliberately smaller bundle; that bundle is not the full
marketplace inventory. The existing `--host claude-code` ZIP still installs
unnamespaced project skills into `.claude/skills/`. Choose one installation method
per target project to avoid exposing duplicate copies of AIEA skills.

Repository `AGENTS.md` and `CLAUDE.md` guide contributors. They are not plugin
startup instructions. Claude's validator may warn about the root `CLAUDE.md`;
the plugin's user-facing instructions are in its skills. Bootstrap bundles a
`references/discovery.md` fallback, copied unchanged into standalone and project
skill packages. It resolves available siblings without assuming the target
application contains the AIEA source tree.

## Smoke check and updates

1. Record `claude --version` and validate both marketplace and plugin manifests.
2. Install from a disposable local marketplace and inspect `claude plugin details aiea`.
   Confirm all nine skills, including all five specialists, appear.
3. In a separate disposable project, invoke `/aiea:aiea-bootstrap` with a read-only
   request. Confirm the skill loads, scopes the request, and reports evidence.
4. Invoke `/aiea:security-review` on a small sample and confirm it makes no edits.
5. Load an extracted plugin ZIP without the original checkout and repeat discovery.

Structural checks and inventory discovery do not prove model behavior. Record
unrun behavioral checks honestly. For hosted updates, bump both `VERSION` and
the plugin manifest version, push the release, then users can run:

```text
/plugin marketplace update aiea-marketplace
/plugin update aiea@aiea-marketplace
```

To remove a test installation, use `claude plugin uninstall aiea@aiea-marketplace`
and `claude plugin marketplace remove aiea-marketplace` with the same configuration
directory used to install it.

## Historical 1.1.0 verification snapshot (2026-10-20)

- Claude Code **2.1.304** accepted both source manifests. Its only warning is the
  expected contributor `CLAUDE.md` warning described above.
- Installation from a local marketplace in an isolated configuration succeeded;
  the plugin was enabled at **1.1.0** and its component inventory listed all nine
  skills, with zero agents, hooks, MCP servers, or LSP servers.
- The extracted standalone plugin passed native validation without warnings.
- Five offline regression tests passed, including all four package targets,
  hash/content checks, deterministic builds, subsets, and rejection cases.
- Model-driven skill invocation and remote GitHub installation have not been
  verified. No release tag or official directory submission has been made.

For the current release, see [verification status](verification-status.md) and
the [manual workflow procedure](workflow-validation.md).

## Official format references

Checked against the documentation on 2026-10-20:

- [Plugin manifest](https://code.claude.com/docs/en/plugins-reference)
- [Create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace)
- [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)

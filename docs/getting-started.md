# Start using AIEA

AIEA supplies 17 engineering skills to your existing coding host. You need a
working, authenticated Claude Code, Codex, or OpenCode installation. Model access,
usage charges, tools, and permissions come from that host. AIEA adds no service,
telemetry, credentials, hooks, or background agent.

The current version is prepared for a **public release**. Packaging is tested; automatic
activation and completed native Claude/OpenCode model workflows remain unverified.
Use explicit activation for your first task and inspect the host's loading evidence.
See [verification status](verification-status.md) for the precise evidence.

## Install in Claude Code

In an interactive Claude Code session, run:

```text
/plugin marketplace add himanshu231204/ai-engineering-army
/plugin install aiea@aiea-marketplace
```

Review the scope offered by Claude Code, then start a new session in your target
project. This installs the default branch, which may advance beyond a release.
For an exact version, download the `claude-code-plugin` ZIP from a published
[GitHub release](https://github.com/himanshu231204/ai-engineering-army/releases),
verify it, and extract it into a separate plugin directory. Start from your target
project using `claude --plugin-dir /absolute/path/to/extracted-plugin`.

Run this in Claude Code:

```text
/aiea:aiea-bootstrap
```

Then send the first-task prompt below. The plugin guide lists
[all skill commands](claude-code-plugin.md#skill-inventory).

## Install in Codex or OpenCode

For installable plugin adapters, use the
[Codex plugin/local marketplace](../adapters/codex/README.md) or
[OpenCode 2 plugin](../adapters/opencode/README.md). Their ZIP names end in
`codex-plugin.zip` and `opencode-plugin.zip`. Both are extracted separately from
your target project. Codex uses its plugin commands; OpenCode 2 uses a `plugins`
configuration entry. Native loading and model-driven use of these new adapters
remain unverified. The OpenCode adapter executes a small local skill-registration
module; it adds no tools, event hooks, or permissions.

The following project-skill installation remains available without a plugin:

Download the matching `codex` or `opencode` ZIP from a published release. Before
extracting, inspect the file list and check for existing skills with the same names.
Both place skills at `.agents/skills/<name>/SKILL.md`. Extract at your target
project's root, keeping the hidden `.agents` folder. Start a new host session there.
No Python is needed to use these installed skills.

If release assets have not been published, build from source with Python 3.10+:

```sh
git clone https://github.com/himanshu231204/ai-engineering-army.git
cd ai-engineering-army
python tools/aiea.py validate
python tools/aiea.py package --host codex
python tools/aiea.py package --host opencode
```

Extract the desired archive from `dist/` into your target project. Do not copy
AIEA's contributor `AGENTS.md` or `CLAUDE.md` over your project's instructions.

Ask the host to load `aiea-bootstrap`. If native discovery is unavailable, ask it
to read `.agents/skills/aiea-bootstrap/SKILL.md` and its referenced discovery file.
That is manual loading; it does not verify automatic selection.

## First task

Start in a disposable project or a clean branch with a small, well-defined change.
For example, give the host this prompt after loading bootstrap:

```text
Use AIEA for this task: fix the failing empty-input validation in my helper.
First inspect this project's instructions, code, and existing tests. State the
expected behavior and run the relevant checks before changing code.
Use a maximum of two repair attempts. Keep tests intact unless a test change is
part of the agreed requirement. If independent reviewers are available, give
them bounded read-only questions; one lead must own all shared-tree edits.
At the end, report files changed, commands and actual results, loaded skills,
and any unresolved or unrun checks. Stop and report incomplete if the budget
is exhausted.
```

Replace the example task with your actual goal and acceptance command. Expect the
host to inspect, choose relevant skills, implement, check, repair within the
budget if needed, and report evidence. AIEA expresses these as instructions; it
does not enforce a sandbox, spawn processes, or guarantee model compliance.

## Check your download

Compare your ZIP's SHA-256 to its entry in `SHA256SUMS` from the same release:

```powershell
Get-FileHash .\aiea-<version>-codex.zip -Algorithm SHA256
```

On Linux use `sha256sum -c SHA256SUMS` with all listed assets present; on macOS
use `shasum -a 256 -c SHA256SUMS`. Checksums detect changes; they are not publisher
signatures. Obtain both assets and checksums from a trusted release source.

## Troubleshooting

| Symptom | What to do |
|---|---|
| Bootstrap is absent | Check the extracted path, installation scope, and enabled plugin; start a new session. Ask the host to show its actual skill inventory. |
| Nothing activates automatically | Invoke bootstrap explicitly, or request the exact installed `SKILL.md`. Automatic selection is host/model behavior. |
| A specialist is missing | Check whether you installed a subset. Bootstrap must report the omission; install a reviewed full package if needed. |
| Independent agents are unavailable | Ask the lead to apply the review contract directly and report that no independent delegation occurred. |
| Host returns 401 or token expired | Authenticate through that host's normal login flow. AIEA does not manage or repair host credentials. |
| Host reports access denied | Check the host's writable state/config directories and your OS permissions. Keep your normal permission controls. |
| A host network request is blocked | Resolve that request through your host/environment's policy. AIEA does not require telemetry or override network controls. |
| Output archive already exists | Choose a new output directory; package and release commands preserve existing output. |

To remove project skills, remove only the AIEA skill directories you installed,
after checking for your own changes. For Claude Code, manage the installed plugin
through `/plugin`. Avoid deleting other project skills or instructions.

Report problems in [GitHub issues](https://github.com/himanshu231204/ai-engineering-army/issues)
with AIEA version, host/version, OS, install method, a sanitized prompt, and actual
results. Never include credentials or private project contents. Use
[the security policy](../SECURITY.md) for vulnerabilities.

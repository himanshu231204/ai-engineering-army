---
name: Evidence Report
about: An issue backed by a captured check run or session transcript
labels: bug, evidence-report
---

<!--
Use this template when a failing check, a captured session transcript, or a
reproducible run proves the problem. Prefer it over Bug Report when you have
that evidence: it lets a maintainer compare your result against their own
without re-running the scenario. For everything else, use Bug Report.
-->

- [ ] I searched existing issues and this is not a duplicate

## Environment (required)

| Field | Value |
|---|---|
| AIEA version or commit | |
| Host (Claude Code, Codex, OpenCode) | |
| Host version | |
| Your model + version | |
| Install method (plugin, ZIP, source checkout) | |
| OS + shell | |

## Is this an AIEA issue or a host issue?

- [ ] I confirmed this issue does not occur with AIEA not loaded

## What happened?

## Steps to reproduce

1.
2.
3.

## Expected behavior

## Actual behavior

## Captured evidence

<!-- The command, its exit code, and the relevant output. Paste it rather
     than describing it. -->

```text

```

<!-- Or attach a session transcript showing the failure. Scrub credentials,
     tokens, and private project content before attaching. -->

## Files changed by the reproduction

<!-- If a repair was attempted, which files did it touch? A bounded repair
     that changed only one file is easier to trust than one that changed
     several. -->

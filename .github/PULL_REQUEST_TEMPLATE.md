<!--
BEFORE SUBMITTING: Read every word of this template. PRs that leave sections
blank, contain multiple unrelated changes, or show no evidence of human
involvement will be closed without review.
-->

> **This PR MUST target `main`.** `main` is the released branch. Releases are
> cut by tagging a commit; a PR does not publish anything.

## Who is submitting this PR? (required)

<!-- Required. PRs that omit this will be closed. We assume an agent wrote this
     PR — tell us which one and where it ran. We weigh contributions by what
     produced them: content reasoned from documentation is held to a different
     bar than work grounded in a real session. -->

| Field | Value |
|---|---|
| Your model + version | |
| Host + version (Claude Code, Codex, OpenCode) | |
| AIEA skills or adapters used while working | |
| Human partner who reviewed this diff | |

## What problem are you trying to solve?

<!-- Describe the specific problem you encountered. If this was a session
     issue, include: what you were doing, what went wrong, the model's exact
     failure mode, and ideally a transcript or session log.

     "Improving" something is not a problem statement. What broke? What failed?
     What was the user experience that motivated this? -->

## What does this PR change?

<!-- 1-3 sentences. What, not why — the "why" belongs above. -->

## Is this change appropriate for core AIEA?

<!-- AIEA v1 is a framework-only, host-neutral skills library. It does not
     include an orchestration engine, application, hosted service, installer,
     telemetry, or benchmark runner. Check the
     [v1 scope](https://github.com/himanshu231204/ai-engineering-army/blob/main/docs/version-1.md)
     and answer:

     - Would this be useful to someone working on a completely different kind
       of project than yours?
     - Is this project-specific, team-specific, or tool-specific?
     - Does it integrate or promote a third-party service?
     - Does it keep the canonical skills host-neutral?

     Host-specific packaging and discovery belong under `adapters/`. -->

## What alternatives did you consider?

<!-- What other approaches did you try or evaluate before landing on this one?
     Why were they worse? If you did not consider alternatives, say so — but
     know that is a red flag. -->

## Does this PR contain multiple unrelated changes?

<!-- If yes: stop. Split it into separate PRs. Bundled PRs will be closed.
     If you believe the changes are related, explain the dependency. -->

## Existing PRs and issues

- [ ] I have reviewed all open AND closed PRs and issues for duplicates or prior art
- Related PRs or issues: <!-- #number, #number, or "none found" -->

<!-- If a related closed PR exists, explain what is different about your
     approach and why it should succeed where the other did not. -->

## Environment tested

| Host | Host version | Model | Model version/ID |
|---|---|---|---|
| | | | |

## New host support (required if this PR adds support for a new host)

<!-- If this PR adds support for a new host (IDE, CLI tool, agent runner),
     you MUST include evidence that the integration actually works.

     A working integration loads the `aiea-bootstrap` skill and the host's
     skill inventory lists every canonical skill. Without that, the skills are
     dead weight — present on disk but never invoked.

     ACCEPTANCE TEST: Start a clean session in the host against this
     repository and ask it to list its available skills. A working
     integration shows all nine skills and loads `aiea-bootstrap` when asked.

     These are NOT real integrations and PRs that ship them will be closed:

     - Manually copying skill files into the host
     - A wrapper that requires the user to opt in per session
     - Anything where `aiea-bootstrap` does not load on request

     If you are not sure whether your integration loads the bootstrap, it does
     not.
-->

<details>
<summary>Clean-session transcript showing the skill inventory</summary>

```text
paste the complete transcript here
```

</details>

## Evidence and verification

<!-- State what you ran and what it actually returned. Record checks you
     could not run as unrun rather than omitting them. -->

| Check | Command | Exit code | Result |
|---|---|---|---|
| Repository validation | `python tools/aiea.py validate` | | |
| Distribution regression checks | `python -m unittest discover -s tests -v` | | |
| Version registry | `python tools/aiea.py version --audit` | | |

<!-- If this PR changes a skill's behavior, also record what you observed
     before and after. -->

- Initial prompt that led to this change:
- Checks run after the change, and how the outcome differed from before:

## Rigor

- [ ] If this is a skill change: I checked the change against the
      [skill quality criteria](https://github.com/himanshu231204/ai-engineering-army/blob/main/docs/skill-catalog.md)
      and the [specialist contracts](https://github.com/himanshu231204/ai-engineering-army/blob/main/docs/specialist-contracts.md)
- [ ] This change was tested against invalid input, not just the happy path
- [ ] I did not modify carefully-tuned content without evidence that the change is an improvement

<!-- If you changed wording in skills that shape agent behavior, show your
     methodology and results. These are not prose — they are evidence. -->

## Human review

- [ ] A human has reviewed the COMPLETE proposed diff before submission

<!--
STOP. If the checkbox above is not checked, do not submit this PR.

PRs will be closed without review if they:
- Show no evidence of human involvement
- Contain multiple unrelated changes
- Promote or integrate third-party services or tools
- Submit project-specific or personal configuration as core changes
- Leave required sections blank or use placeholder text
- Change behavior-shaping content without evidence
-->

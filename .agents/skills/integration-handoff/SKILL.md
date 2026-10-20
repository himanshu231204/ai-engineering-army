---
name: integration-handoff
description: Use when finishing an engineering change, integrating scoped review findings, or handing a patch to another developer, especially when tests are blocked, work is partial, or publication still needs a separate step.
license: MIT
---

# Integration and handoff

Make the result reviewable without asking the next developer to reconstruct the
conversation. A prepared patch and a published change are different states.

1. Confirm the final diff, ownership of changed files, and whether delegated
   work has finished. The lead alone integrates accepted shared-tree changes.
   Resolve conflicting recommendations from evidence and record material risks.
2. Collect actual check commands/results, relevant versions, and the repair
   count/budget. Use evidence verification; do not rerun expensive checks without
   a reason, or count an unavailable check as passed.
3. State the observed outcome and what changed, why, and where. Distinguish
   implemented behavior from design recommendations and future work.
4. List remaining failures, blocked/unrun checks, and the smallest concrete next
   action. If the budget expired, say incomplete. If files are only staged or
   packaged, do not claim they were applied, committed, pushed, or deployed.
5. For a patch/package, identify its base, contents, verification, and exact
   application or installation command. Preserve existing output and user edits;
   ask before irreversible or external actions unless already authorized.
6. Return a concise developer handoff: outcome, changed files, verification,
   unresolved risks, and next action. Scale detail to the size of the change.

**Boundary:** This skill does not itself authorize Git writes, merging, sending
messages, or deployment. Do not conceal blockers behind a completion claim.

# Contributing

Contributions should improve portable engineering workflows with clear scope and evidence. Start with a focused issue or pull request description that states the user problem and expected behavior. Check the framework-only scope in [version 1](version-1.md) before proposing a new component.

## Skill contributions

- Put every canonical skill directly under `.agents/skills/<skill-name>/SKILL.md`.
- Register its name and core/specialist group in `skill-registry.json`; do not create grouping subdirectories.
- Register any file that carries the repository version in `.version-bump.json`; run `python tools/aiea.py version --check` to confirm the declared files still agree.
- Use a lowercase hyphenated folder and matching frontmatter `name`.
- Write a specific `description` that explains the task and when the skill applies.
- Keep the workflow host-neutral. Put host setup or packaging details under `adapters/`.
- Define boundaries, expected outputs, and verification where relevant.
- Keep specialist contracts concise and default them to read-only analysis.
- Include small, sanitized fixtures only when they clarify behavior. Do not add secrets or user data.

## Tooling and documentation

- Use the standard-library CLI; do not add a dependency for a check that can remain deterministic and local.
- Update host compatibility docs when verified host paths or behavior change.
- Update `VERSION` and `CHANGELOG.md` only for an intentional release.
- Keep version, architecture, adapters, and README claims consistent.

## Before opening a pull request

The pull request template asks for the problem, the change, the checks you ran
with their exit codes, and the human who reviewed the diff. Complete it
honestly: sections left blank or filled with placeholder text will be closed
without review.

- Run `python tools/aiea.py validate`.
- Run `python -m unittest discover -s tests -v`.
- Run `python tools/aiea.py version --audit` if the change touches a version-bearing file.
- If packaging changes, build and inspect archives for all affected hosts.
- Review the diff for accidental credentials, unrelated files, and unsupported claims.
- Describe checks performed and outcomes; do not claim checks that were not run.
- Keep one change per pull request, and have a human review the complete diff.

Issues use the templates under `.github/ISSUE_TEMPLATE/`. Bug reports ask for
the host, the model, and the command that failed; a feature request asks
whether the change fits the framework-only scope. Use Discussions for usage
questions rather than opening an issue.

By contributing, you agree that your contributions are provided under the repository's MIT license.

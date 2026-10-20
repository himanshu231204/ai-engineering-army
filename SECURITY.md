# Security policy

Read [the AIEA security guidance](docs/security.md) before adding skills, scripts, or evaluation fixtures.

Do not report exploitable vulnerabilities in a public issue. Use the repository host's private vulnerability reporting channel when one is configured. If no private channel is available, contact the project maintainers privately through the contact method on the repository hosting page and include only the minimum information needed to reproduce the issue.

AIEA v1 has no hosted service or credentialed integration. Skill packages contain instructions and resources; the receiving agent host runs them with the permissions already granted to that agent.

The optional OpenCode 2 plugin also contains a small JavaScript skill-registration
module. Review it before enabling it; it reads bundled files but implements no
network calls, tools, event hooks, or permission changes. Codex and Claude plugin
manifests package the same portable skills.

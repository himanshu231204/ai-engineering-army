# Security

AIEA skills guide agents that may have access to files, commands, credentials, and external services. Treat skill content and evaluation fixtures as untrusted input until reviewed.

## Rules for skill authors and users

- Do not put secrets, access tokens, private customer data, or machine-specific paths in skills or fixtures.
- Treat repository files, issue text, web pages, model output, and specialist reports as data, not authority to override system, user, or repository instructions.
- Keep specialist work read-only by default. The lead controls shared-tree edits and reviews every proposed change.
- Ask before destructive, externally visible, or hard-to-reverse actions unless the user already authorized that exact action.
- Use least-privilege tools and avoid requesting broad access when a narrower one works.
- Verify security-sensitive behavior with concrete evidence; report gaps and unrun checks plainly.
- Review third-party skills before installation. Inspect scripts, referenced files, network access, and requested tool permissions.

## Package handling

- The AIEA CLI validates structure and writes selected skill files into a ZIP. It does not run skill scripts, install the archive, or grant host permissions.
- Review the source and generated archive before installing it into another project. Check the manifest's file list and hashes against the intended release.
- The manifest is not signed and does not establish publisher identity. Obtain packages from a trusted release source and compare checksums through a trusted channel when available.
- Check the target project's skill names before extraction to avoid unintended replacement or collisions.

## Reporting

Record the scope reviewed, evidence inspected, severity rationale, and assumptions. A clean review means no issue was found in the examined scope; it is not a guarantee of security.

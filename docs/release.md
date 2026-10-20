# Release procedure

This document defines the v1 release process. Publishing a GitHub release requires a configured remote and maintainer credentials; local package generation does not.

## Prepare

1. Confirm the intended version and update both `VERSION` and `.claude-plugin/plugin.json` using the same semantic version. The plugin version controls hosted update detection.
2. Add a dated entry to `CHANGELOG.md` describing user-visible changes.
3. Review the canonical skills, agent instructions, docs, fixtures, and current host compatibility references.
4. Run validation and generate all host packages:

   ```sh
   python tools/aiea.py validate
   python -m unittest discover -s tests -v
   python tools/aiea.py package --host claude-code-plugin --output .tmp/release
   python tools/aiea.py package --host claude-code --output .tmp/release
   python tools/aiea.py package --host codex --output .tmp/release
   python tools/aiea.py package --host opencode --output .tmp/release
   ```

5. Inspect the manifests and archive contents. Confirm the package includes only the intended skills and paths.
6. Smoke-check discovery in each supported host when available. Record host versions and results; a ZIP build alone is not proof that a host loaded the skills.

Also run `claude plugin validate .` and
`claude plugin validate .claude-plugin/plugin.json`, then follow the
[plugin smoke checklist](claude-code-plugin.md#smoke-check-and-updates).
Record CLI version, inventory results, and any warnings. Validate the standalone
ZIP after extraction too. Passing metadata validation is not behavioral proof.

## Publish

1. Review the complete diff and confirm the working tree contains only release changes.
2. Commit the release changes and tag the commit `v<VERSION>`.
3. If a GitHub remote is configured, attach the four ZIP packages and changelog entry to the release.
4. Push the marketplace files to the default branch before advertising GitHub installation commands. Official Anthropic directory submission is separate.
5. Do not publish credentials, private evaluation data, or unreviewed third-party skills.

If a host smoke check is unavailable, state that limitation in the release notes instead of marking it verified.

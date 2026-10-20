# Release procedure

This document defines the v1 release process. Publishing a GitHub release requires a configured remote and maintainer credentials; local package generation does not.

An unreleased candidate may already carry its intended version in `VERSION` and
the plugin manifest. Keep its changelog entry marked Unreleased until publishing.
A dated source entry does not itself establish a hosted release or tag.

## Current release policy

Prepare 1.1.1 as a **public preview**, with GitHub's prerelease flag. Developers
can install the default-branch marketplace or use reviewed versioned ZIPs once
published. Do not advertise automatic triggering or completed native
Claude/OpenCode workflows as verified. The current host blockers are documented
in [verification status](verification-status.md), not silently treated as passes.
Update [release notes](release-notes.md) when evidence or limitations change.

## Prepare

1. Confirm the intended version and update both `VERSION` and `.claude-plugin/plugin.json` using the same semantic version. The plugin version controls hosted update detection.
2. Review `CHANGELOG.md` and `docs/release-notes.md` for user-visible changes and actual verification limits. Date the changelog entry when publishing.
3. Review the canonical skills, agent instructions, docs, fixtures, and current host compatibility references.
4. Run validation and generate all host packages:

   ```sh
   python tools/aiea.py validate
   python -m unittest discover -s tests -v
   python tools/aiea.py release
   ```

5. Inspect `dist/release-<VERSION>/`: four ZIPs, `RELEASE-NOTES.md`, and `SHA256SUMS`. Confirm the manifests include only intended skills and paths and the hashes match. Every archive carries the MIT license; project packages use `AIEA-LICENSE.txt` to preserve a consumer's own `LICENSE`.
6. Follow `docs/workflow-validation.md` and update `docs/verification-status.md` with
   the source commit, host versions, actual discovery inventories, and observed
   repair/delegation behavior. Record unavailable checks as unrun.

Also run `claude plugin validate .` and
`claude plugin validate .claude-plugin/plugin.json`, then follow the
[plugin smoke checklist](claude-code-plugin.md#smoke-check-and-updates).
Record CLI version, inventory results, and any warnings. Validate the standalone
ZIP after extraction too. Passing metadata validation is not behavioral proof.

## Publish

1. Review the complete diff and confirm the working tree contains only release changes.
2. Commit the release changes and tag the commit `v<VERSION>`.
3. If a GitHub remote is configured, create a draft prerelease and attach all six prepared assets. Use the prepared notes as the description, including the host limitations. Review the draft before publishing it.
4. Push the marketplace files to the default branch before advertising GitHub installation commands. Official Anthropic directory submission is separate.
5. Do not publish credentials, private evaluation data, or unreviewed third-party skills.

If a host smoke check is unavailable, state that limitation in the release notes instead of marking it verified.

For 1.1.1, after reviewing and committing the changes, maintainers can run:

```sh
git tag v1.1.1
git push origin main v1.1.1
gh release create v1.1.1 dist/release-1.1.1/* --verify-tag --draft --prerelease --title "AIEA 1.1.1 public preview" --notes-file dist/release-1.1.1/RELEASE-NOTES.md
```

These are publishing steps for the maintainer, not commands run by `aiea release`.
If a tag already exists, inspect it rather than moving or replacing it. Build
the assets from the exact source being tagged. After editing release notes,
rebuild in a fresh output directory so the packaged notes and checksums agree.

CI validates on Linux and Windows with Python 3.10 and 3.12, prepares the bundle,
and uploads it as a workflow artifact. This does not publish a GitHub release.
Review all matrix results and use assets from the intended source commit.

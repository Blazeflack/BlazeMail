# Releasing BlazeMail

1. Update `## Version:` in `BlazeMail.toc` and add the matching dated entry to
   `CHANGELOG.md`. Keep versions aligned; the repository migration does not
   change the addon version.
2. Commit and push the changes to `main`. Wait for Validate addon to pass.
3. Create and push a new tag in the format `vX.Y.Z`.
4. Check both the GitHub release and the CurseForge packaging result, including
   release type, Forever game version, release notes and ZIP contents.

Ordinary pushes do not publish a release. Existing releases are never overwritten.
Historical releases remain in https://github.com/Blazeflack/WoW-AddOns/releases.
Old addon-prefixed tags are not copied into this repository.

## Local package validation

Run from this repository with Python 3.8 or newer:

```text
python .github/scripts/package_addon.py vX.Y.Z --output-dir <outside-repository-directory>
```

The ZIP contains exactly one `BlazeMail/` folder and the files required by its TOC.
Development references, tests, workflows and screenshots are omitted.
This verifies packaging, not behavior in WoW Forever.

## Preparing release notes

`CHANGELOG.md` is the single source for release notes. Keep the newest version
first and retain previous versions below it. The package check requires a
nonempty entry matching the TOC and tag version.

`.pkgmeta` tells CurseForge to display the entire `CHANGELOG.md` as Markdown
instead of generating notes from commit messages. GitHub also displays the full
changelog, with installation instructions added above it. Each release includes
the history as it existed in its tagged commit; older releases are not updated
when later entries are added. Both ZIPs include `CHANGELOG.md`.

CurseForge reads the file directly from the tagged commit and does not wait for
GitHub Actions. Commit the updated changelog before pushing the tag.

Packaging reference:
https://support.curseforge.com/support/solutions/articles/9000197952-preparing-the-packagemeta-file

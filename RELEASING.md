# Releasing BlazeMail

1. Update `## Version:` in `BlazeMail.toc` and add the matching dated entry to
   `CHANGELOG.md`. Keep versions aligned; the repository migration does not
   change the addon version.
2. Commit and push the changes to `main`.
3. Create and push a new tag in the format `vX.Y.Z`.
4. Check the Release addon workflow and its published GitHub release.

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

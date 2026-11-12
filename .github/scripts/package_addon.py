"""Build one installable addon ZIP, validating its tag against the TOC."""

import argparse
import os
from pathlib import Path
import re
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile


def package(tag, output_dir):
    match = re.fullmatch(
        r"v(\d+\.\d+\.\d+)", tag
    )
    if not match:
        raise ValueError("Expected tag vX.Y.Z")
    addon, version = "BlazeMail", match.group(1)
    root = Path(__file__).resolve().parents[2]
    toc_path = root / f"{addon}.toc"
    toc = toc_path.read_text(encoding="utf-8-sig")
    toc_version = re.search(r"^## Version:\s*(\S+)\s*$", toc, re.MULTILINE)
    if not toc_version or toc_version.group(1) != version:
        raise ValueError(f"Tag version {version} does not match {toc_path.name}")

    tracked = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root
    ).decode("utf-8").split("\0")
    files = []
    for name in filter(None, tracked):
        path = Path(name)
        if any(part.startswith(".") or part.lower() in {"test", "tests", "__pycache__", "images"} for part in path.parts):
            continue
        if path.name.lower() in {"api.json", "agents.md", ".gitignore", "development.md", "releasing.md"}:
            continue
        source = root / path
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Not a regular file: {name}")
        files.append(path.as_posix())

    required = {f"{addon}.toc", "HOW_TO_USE.txt", "CHANGELOG.md", "LICENSE"}
    for line in toc.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            required.add(line.replace(chr(92), "/"))
    if missing := required.difference(files):
        raise ValueError(f"Required files missing from package: {sorted(missing)}")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8-sig")
    section = re.search(
        rf"^## {re.escape(version)}(?:\s+-[^\n]*)?\s*\n(.*?)(?=^## |\Z)",
        changelog, re.MULTILINE | re.DOTALL,
    )
    if not section or not section.group(1).strip():
        raise ValueError(f"Missing changelog entry for {version}")

    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{addon}-{version}.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for name in sorted(files):
            bundle.write(root / name, f"{addon}/{name}")
    with ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
        if {name.split('/')[0] for name in bundle.namelist()} != {addon}:
            raise ValueError("ZIP must contain exactly one addon folder")

    notes = output_dir / f"{addon}-{version}-notes.md"
    notes.write_text(
        f"## Installation\n\nDownload **{archive.name}** and extract the **{addon}/** "
        "folder into `Interface/AddOns`.\n\n"
        "See `HOW_TO_USE.txt` inside the addon folder for usage instructions.\n\n"
        + changelog.strip() + "\n",
        encoding="utf-8",
    )
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write(f"title={addon} {version}\narchive={archive}\nnotes={notes}\n")
    print(f"Validated {archive.name}: {len(files)} files, one addon folder, no tests")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    package(args.tag, args.output_dir)

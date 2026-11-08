"""Does a built wheel carry every data file the package reads at run time?

Every install of this package is editable (``pip install -e``), and an editable
install reads straight from the checkout -- so a data file missing from
``[tool.setuptools.package-data]`` is invisible until somebody builds a real
wheel, and then the console answers 404, ``retrieve_config`` raises, or the
recorder goes silent with nothing raising to say why.

So this compares a wheel against ``git ls-files``, not against a list of its
own: each directory below must arrive in the wheel WHOLE, file for file. A new
asset added to one of them is covered without editing this script; a new
directory of data is one line in ``DATA_DIRS``.

Run through the Makefile, which builds the wheel first::

    make check-wheel
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Directories (relative to the repo) holding files that are read at run time
# and are not Python, so package discovery alone never ships them.
DATA_DIRS: "tuple[str, ...]" = (
    "actoris_harena/recording/sounds",
    "actoris_harena/web/static",
    "actoris_harena/configuration",
    "actoris_harena/arena/raven/environments/assets",
    "actoris_harena/arena/deformable_raven/src/assets",
)


def tracked(directory: str) -> "set[str]":
    out = subprocess.run(
        ["git", "ls-files", "-z", directory],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout.decode()
    return {p for p in out.split("\0") if p and not p.endswith(".py")}


def missing_from(wheel: Path) -> "dict[str, list[str]]":
    names = set(zipfile.ZipFile(wheel).namelist())
    gaps: "dict[str, list[str]]" = {}
    for directory in DATA_DIRS:
        files = tracked(directory)
        if not files:
            gaps[directory] = ["<git tracks nothing here -- stale DATA_DIRS entry?>"]
            continue
        absent = sorted(files - names)
        if absent:
            gaps[directory] = absent
    return gaps


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("wheel_dir", type=Path, help="directory holding one .whl")
    args = parser.parse_args()

    wheels = sorted(args.wheel_dir.glob("actoris_harena-*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"❌ expected one actoris_harena wheel in {args.wheel_dir}, found {len(wheels)}")

    gaps = missing_from(wheels[0])
    if gaps:
        for directory, absent in gaps.items():
            print(f"❌ {directory}: {len(absent)} file(s) not in the wheel, e.g. {absent[0]}")
        raise SystemExit("   add them to [tool.setuptools.package-data] in pyproject.toml")
    print(f"✓ {wheels[0].name} carries every data file in {len(DATA_DIRS)} directories")


if __name__ == "__main__":
    sys.exit(main())

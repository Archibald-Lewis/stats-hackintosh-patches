#!/usr/bin/env python3
"""Apply or check the patch against the exact supported Stats source revision."""
import argparse
from pathlib import Path
import subprocess

BASE = "5cf09a8cb0561ff24c28be4e5374d579d0601818"
PATCH = Path(__file__).resolve().parents[1] / "patches/stats-3.0.23-hackintosh.patch"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="A clean checkout of exelban/stats v3.0.23")
    parser.add_argument("--check", action="store_true", help="Validate without modifying files")
    args = parser.parse_args()
    repo = args.source.resolve()
    head = git(repo, "rev-parse", "HEAD")
    if head.returncode or head.stdout.strip() != BASE:
        raise SystemExit("Use Stats v3.0.23 at commit " + BASE)
    status = git(repo, "status", "--porcelain")
    if status.returncode:
        raise SystemExit(status.stderr)
    if status.stdout.strip():
        raise SystemExit("The source checkout has local changes. Use a clean checkout; no changes made.")
    check = git(repo, "apply", "--check", str(PATCH))
    if check.returncode:
        raise SystemExit(check.stderr)
    if args.check:
        print("Patch applies cleanly. No files changed.")
        return
    applied = git(repo, "apply", str(PATCH))
    if applied.returncode:
        raise SystemExit(applied.stderr)
    print("Applied to", repo)


if __name__ == "__main__":
    main()

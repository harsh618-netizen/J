#!/usr/bin/env python3
"""Find duplicate files by comparing SHA-256 hashes."""

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(root: Path) -> dict[str, list[Path]]:
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file():
            try:
                by_size[path.stat().st_size].append(path)
            except OSError:
                continue

    hashes: dict[str, list[Path]] = defaultdict(list)
    for candidates in by_size.values():
        if len(candidates) < 2:
            continue
        for path in candidates:
            try:
                hashes[sha256_file(path)].append(path)
            except OSError:
                continue

    return {file_hash: paths for file_hash, paths in hashes.items() if len(paths) > 1}


def print_report(duplicates: dict[str, list[Path]]) -> None:
    if not duplicates:
        print("No duplicate files found.")
        return

    total = 0
    for index, (file_hash, paths) in enumerate(sorted(duplicates.items()), start=1):
        print(f"Group {index} | SHA-256: {file_hash}")
        for path in paths:
            print(f"  - {path}")
        total += len(paths) - 1
        print()
    print(f"Duplicate copies found: {total}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find duplicate files in a directory using size and SHA-256."
    )
    parser.add_argument("directory", type=Path, help="Directory to scan")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.directory.is_dir():
        raise SystemExit(f"Not a directory: {args.directory}")
    print_report(find_duplicates(args.directory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

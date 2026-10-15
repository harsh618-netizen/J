#!/usr/bin/env python3
"""Analyze disk usage under a directory without changing any files."""

from __future__ import annotations

import argparse
from pathlib import Path


def folder_sizes(root: Path) -> list[tuple[Path, int]]:
    """Return immediate subdirectories and their recursive sizes, largest first."""
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    results: list[tuple[Path, int]] = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        total = 0
        for path in child.rglob("*"):
            try:
                if path.is_file():
                    total += path.stat().st_size
            except (OSError, PermissionError):
                # Skip files that disappear or cannot be read during scanning.
                continue
        results.append((child, total))
    return sorted(results, key=lambda item: item[1], reverse=True)


def human_size(size: int) -> str:
    """Format bytes in a readable binary unit."""
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Show which immediate subfolders use the most disk space."
    )
    parser.add_argument("directory", nargs="?", default=".", help="Folder to analyze")
    parser.add_argument("--top", type=int, default=10, help="Number of folders to show (default: 10)")
    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1")

    try:
        results = folder_sizes(Path(args.directory))
    except (NotADirectoryError, OSError) as exc:
        parser.error(str(exc))

    if not results:
        print("No subfolders found.")
        return 0

    print(f"{'SIZE':>12}  FOLDER")
    print("-" * 60)
    for folder, size in results[: args.top]:
        print(f"{human_size(size):>12}  {folder.name}")
    print(f"\nScanned {len(results)} subfolder(s). No files were changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

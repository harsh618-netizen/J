"""Smart File Organizer - safely organize files by extension."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

CATEGORY_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".csv", ".xlsx"},
    "Audio": {".mp3", ".wav", ".m4a", ".flac"},
    "Video": {".mp4", ".mkv", ".mov", ".avi"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp"},
}


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORY_MAP.items():
        if suffix in extensions:
            return category
    return "Others"


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool = False) -> list[tuple[Path, Path]]:
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Folder does not exist: {folder}")

    moves: list[tuple[Path, Path]] = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        destination_folder = folder / category_for(item)
        destination = unique_destination(destination_folder / item.name)
        moves.append((item, destination))
        if not dry_run:
            destination_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
    return moves


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files in a folder by type.")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview moves without changing files")
    args = parser.parse_args()

    moves = organize(Path(args.folder).expanduser().resolve(), dry_run=args.dry_run)
    if not moves:
        print("No files found to organize.")
        return

    prefix = "Planned" if args.dry_run else "Moved"
    for source, destination in moves:
        print(f"{prefix}: {source.name} -> {destination.parent.name}/{destination.name}")
    print(f"\n{len(moves)} file(s) processed.")


if __name__ == "__main__":
    main()

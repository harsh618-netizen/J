from pathlib import Path
import shutil

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".csv", ".ppt", ".pptx"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}


def get_category(extension: str) -> str:
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def organize(folder: Path) -> int:
    moved = 0
    for item in folder.iterdir():
        if not item.is_file() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        destination = folder / category
        destination.mkdir(exist_ok=True)

        target = destination / item.name
        counter = 1
        while target.exists():
            target = destination / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        shutil.move(str(item), str(target))
        moved += 1
        print(f"Moved: {item.name} -> {category}/")

    return moved


def main() -> None:
    raw = input("Enter the folder path to organize: ").strip().strip('"')
    folder = Path(raw).expanduser()

    if not folder.is_dir():
        print("Error: folder not found.")
        return

    moved = organize(folder)
    print(f"\nDone! Organized {moved} file(s).")


if __name__ == "__main__":
    main()

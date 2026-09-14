"""CSV Data Cleaner - normalize and validate simple CSV files."""

import csv
import sys
from pathlib import Path


def clean_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    """Trim whitespace, normalize blank values, and remove duplicate rows."""
    cleaned = []
    seen = set()
    duplicates = 0

    for row in rows:
        normalized = {
            (key or "").strip(): (value or "").strip()
            for key, value in row.items()
        }
        fingerprint = tuple(sorted(normalized.items()))
        if fingerprint in seen:
            duplicates += 1
            continue
        seen.add(fingerprint)
        cleaned.append(normalized)

    return cleaned, duplicates


def clean_csv(input_path: str, output_path: str) -> tuple[int, int]:
    """Clean input CSV and write output CSV. Returns (rows_written, duplicates_removed)."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with source.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV must include a header row.")
        rows, _ = clean_rows(list(reader))

    fieldnames = [name.strip() for name in reader.fieldnames]
    with Path(output_path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    original_count = sum(1 for _ in source.open("r", encoding="utf-8")) - 1
    return len(rows), max(0, original_count - len(rows))


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python csv_data_cleaner.py input.csv cleaned.csv")
        raise SystemExit(2)

    try:
        rows_written, duplicates_removed = clean_csv(sys.argv[1], sys.argv[2])
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)

    print(f"Cleaned CSV written to: {sys.argv[2]}")
    print(f"Rows written: {rows_written}")
    print(f"Duplicates removed: {duplicates_removed}")


if __name__ == "__main__":
    main()

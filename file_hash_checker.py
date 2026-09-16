"""File integrity checker using SHA-256 hashes."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def calculate_sha256(file_path: str, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 hash of a file without loading it all into memory."""
    digest = hashlib.sha256()
    with Path(file_path).open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate or verify a file's SHA-256 hash.")
    parser.add_argument("file", help="Path to the file")
    parser.add_argument("--expected", help="Expected SHA-256 hash to verify")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        parser.error(f"File not found: {path}")

    actual = calculate_sha256(str(path))
    print(f"SHA-256: {actual}")

    if args.expected:
        matches = actual.lower() == args.expected.strip().lower()
        print("Status: MATCH" if matches else "Status: MISMATCH")
        raise SystemExit(0 if matches else 1)


if __name__ == "__main__":
    main()

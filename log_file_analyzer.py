#!/usr/bin/env python3
"""Analyze simple web/application log files using only the standard library."""

import argparse
import re
from collections import Counter
from pathlib import Path

LEVELS = ("ERROR", "WARNING", "WARN", "INFO", "DEBUG")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def analyze_lines(lines: list[str]) -> dict:
    counts = Counter()
    ips = Counter()

    for line in lines:
        upper = line.upper()
        matched_level = next((level for level in LEVELS if level in upper), "OTHER")
        counts[matched_level] += 1

        for ip in IP_RE.findall(line):
            ips[ip] += 1

    total = sum(counts.values())
    return {"total_lines": total, "levels": counts, "top_ips": ips.most_common(10)}


def analyze_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return analyze_lines(handle.readlines())


def print_report(path: Path, report: dict) -> None:
    print(f"File: {path}")
    print(f"Total lines: {report['total_lines']}")
    print("\nLevels:")
    for level, count in sorted(report["levels"].items()):
        print(f"  {level:<8} {count}")

    print("\nTop IP addresses:")
    if not report["top_ips"]:
        print("  No IP addresses found")
    else:
        for ip, count in report["top_ips"]:
            print(f"  {ip:<15} {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a text log file.")
    parser.add_argument("file", type=Path, help="Path to a log file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.file.is_file():
        raise SystemExit(f"File not found: {args.file}")

    print_report(args.file, analyze_file(args.file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

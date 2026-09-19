#!/usr/bin/env python3
"""A small JSON-backed habit tracker for the command line."""

import argparse
import json
from datetime import date, timedelta
from pathlib import Path


DEFAULT_FILE = Path("habits.json")


def load_data(path: Path) -> dict:
    if not path.exists():
        return {"habits": {}}
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("habits", {}), dict):
        raise ValueError("Data file must contain a 'habits' object")
    return data


def save_data(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def add_habit(data: dict, name: str) -> None:
    key = name.strip()
    if not key:
        raise ValueError("Habit name cannot be empty")
    if key in data["habits"]:
        raise ValueError(f"Habit already exists: {key}")
    data["habits"][key] = {"completed": []}


def mark_habit(data: dict, name: str, day: str | None = None) -> None:
    if name not in data["habits"]:
        raise ValueError(f"Unknown habit: {name}")
    target = day or date.today().isoformat()
    date.fromisoformat(target)
    completed = data["habits"][name]["completed"]
    if target not in completed:
        completed.append(target)
        completed.sort()


def current_streak(completed: list[str], today: date | None = None) -> int:
    if not completed:
        return 0
    today = today or date.today()
    completed_dates = {date.fromisoformat(day) for day in completed}
    cursor = today
    streak = 0
    while cursor in completed_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def print_status(data: dict) -> None:
    if not data["habits"]:
        print("No habits yet. Add one with: python habit_tracker.py add \"Read\"")
        return
    today = date.today()
    for name, info in data["habits"].items():
        done_today = today.isoformat() in info.get("completed", [])
        marker = "✓" if done_today else "-"
        streak = current_streak(info.get("completed", []), today)
        print(f"{marker} {name} | streak: {streak} day(s)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track daily habits locally in JSON.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="JSON storage file")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new habit")
    add_parser.add_argument("name")

    done_parser = subparsers.add_parser("done", help="Mark a habit as completed")
    done_parser.add_argument("name")
    done_parser.add_argument("--date", dest="day", help="Date in YYYY-MM-DD format")

    subparsers.add_parser("status", help="Show today's status and current streaks")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        data = load_data(args.file)
        if args.command == "add":
            add_habit(data, args.name)
            save_data(args.file, data)
            print(f"Added habit: {args.name.strip()}")
        elif args.command == "done":
            mark_habit(data, args.name, args.day)
            save_data(args.file, data)
            print(f"Marked complete: {args.name}")
        else:
            print_status(data)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

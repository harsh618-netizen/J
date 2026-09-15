"""JSON Toolkit: validate, pretty-print, and flatten JSON data."""

import argparse
import json
from typing import Any


def flatten_json(data: Any, parent_key: str = "", separator: str = ".") -> dict[str, Any]:
    """Flatten nested dictionaries/lists into dotted keys."""
    items: dict[str, Any] = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else str(key)
            items.update(flatten_json(value, new_key, separator))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_key = f"{parent_key}{separator}{index}" if parent_key else str(index)
            items.update(flatten_json(value, new_key, separator))
    else:
        items[parent_key] = data
    return items


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate, format, or flatten a JSON file.")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("--output", help="Output file for formatted JSON")
    parser.add_argument("--flatten", action="store_true", help="Print flattened key-value pairs")
    args = parser.parse_args()

    try:
        data = load_json(args.input)
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")
        raise SystemExit(1)
    except OSError as error:
        print(f"Could not read file: {error}")
        raise SystemExit(1)

    if args.flatten:
        for key, value in flatten_json(data).items():
            print(f"{key} = {value}")
    elif args.output:
        save_json(args.output, data)
        print(f"Formatted JSON saved to {args.output}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

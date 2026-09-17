"""Generate a Markdown table of contents from ATX-style headings."""

import argparse
import re
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def slugify(text: str) -> str:
    """Create a GitHub-style-ish anchor slug."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text.strip().lower()).strip("-")


def extract_headings(markdown: str) -> list[tuple[int, str]]:
    """Return (heading_level, heading_text) pairs."""
    headings = []
    in_fence = False
    for line in markdown.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((len(match.group(1)), match.group(2).rstrip("#").strip()))
    return headings


def build_toc(headings: list[tuple[int, str]], max_level: int = 3) -> str:
    """Build a nested Markdown bullet list."""
    lines = []
    used_slugs: dict[str, int] = {}
    for level, text in headings:
        if level > max_level:
            continue
        slug = slugify(text)
        used_slugs[slug] = used_slugs.get(slug, 0) + 1
        if used_slugs[slug] > 1:
            slug = f"{slug}-{used_slugs[slug] - 1}"
        lines.append(f"{'  ' * (level - 1)}- [{text}](#{slug})")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Markdown table of contents.")
    parser.add_argument("input", type=Path, help="Markdown file to scan")
    parser.add_argument("-o", "--output", type=Path, help="Optional file for the generated TOC")
    parser.add_argument("--max-level", type=int, choices=range(1, 7), default=3)
    args = parser.parse_args()

    markdown = args.input.read_text(encoding="utf-8")
    toc = build_toc(extract_headings(markdown), args.max_level)
    if args.output:
        args.output.write_text(toc + ("\n" if toc else ""), encoding="utf-8")
        print(f"TOC written to {args.output}")
    else:
        print(toc)


if __name__ == "__main__":
    main()

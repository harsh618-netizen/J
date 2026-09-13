"""Text Analyzer - a simple local CLI utility for students and writers."""

import re
import sys


def analyze_text(text: str) -> dict[str, int | float]:
    """Return useful statistics for a piece of text."""
    words = re.findall(r"\b[\w'-]+\b", text)
    sentences = [part for part in re.split(r"[.!?]+", text) if part.strip()]
    characters_no_spaces = sum(not char.isspace() for char in text)
    paragraphs = [part for part in re.split(r"\n\s*\n", text) if part.strip()]
    word_count = len(words)
    reading_time_minutes = round(word_count / 200, 2) if word_count else 0

    return {
        "words": word_count,
        "characters": len(text),
        "characters_no_spaces": characters_no_spaces,
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "reading_time_minutes": reading_time_minutes,
    }


def main() -> None:
    print("📝 Text Analyzer")
    print("Paste your text below. Press Enter twice on an empty line to analyze.\n")

    lines: list[str] = []
    while True:
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            break
        if not line and lines and lines[-1] == "":
            break
        lines.append(line)

    text = "\n".join(lines).strip()
    stats = analyze_text(text)

    print("\nResults")
    print(f"Words: {stats['words']}")
    print(f"Characters: {stats['characters']}")
    print(f"Characters (no spaces): {stats['characters_no_spaces']}")
    print(f"Sentences: {stats['sentences']}")
    print(f"Paragraphs: {stats['paragraphs']}")
    print(f"Estimated reading time: {stats['reading_time_minutes']} minute(s)")


if __name__ == "__main__":
    main()

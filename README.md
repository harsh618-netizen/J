# Python Mini Projects

This repository contains small, practical Python projects for learning and portfolio building.

## Projects

### 🔐 Password Strength Checker
A local-only CLI utility that scores password strength and gives security suggestions.

Run:

```bash
python password_strength_checker.py
```

### 💰 Daily Expense Tracker
A local CLI expense tracker that saves records to `expenses.csv` and prints total spending by category.

Run:

```bash
python daily_expense_tracker.py
```

### 📝 Text Analyzer
A local CLI utility that counts words, characters, sentences, paragraphs, and estimated reading time.

Run:

```bash
python text_analyzer.py
```

### 🧹 CSV Data Cleaner
A practical utility that trims whitespace, normalizes CSV values, removes duplicate rows, and writes a cleaned output file.

Run:

```bash
python csv_data_cleaner.py input.csv cleaned.csv
```

### 🧰 JSON Toolkit
A command-line utility to validate JSON, pretty-print it, save formatted output, and flatten nested objects into dotted keys.

Examples:

```bash
python json_toolkit.py data.json
python json_toolkit.py data.json --output formatted.json
python json_toolkit.py data.json --flatten
```

### 🛡️ File Integrity Checker
A lightweight cybersecurity utility that calculates a file's SHA-256 hash and can verify it against an expected hash.

Examples:

```bash
python file_hash_checker.py example.zip
python file_hash_checker.py example.zip --expected <sha256-hash>
```

### 📚 Markdown TOC Generator
A developer utility that scans Markdown headings and generates a clean table of contents with anchor links.

Examples:

```bash
python markdown_toc_generator.py README.md
python markdown_toc_generator.py README.md --output toc.md
```

### 🌐 URL Health Checker
A standard-library CLI tool that checks whether websites are reachable and reports HTTP status codes and response time. Multiple URLs can be checked concurrently.

Examples:

```bash
python url_health_checker.py example.com https://github.com
python url_health_checker.py example.com example.org --timeout 3 --workers 2
```

### 📊 Log File Analyzer
A beginner-friendly log analysis utility that counts log levels, finds frequent IP addresses, and produces a simple terminal report.

Example:

```bash
python log_file_analyzer.py app.log
```

### ✅ Habit Tracker
A local JSON-backed CLI for creating habits, marking them complete, and viewing current streaks. It uses only the Python standard library.

Examples:

```bash
python habit_tracker.py add "Read 20 pages"
python habit_tracker.py done "Read 20 pages"
python habit_tracker.py status
python habit_tracker.py --file my_habits.json status
```

Dates can be supplied for testing or backfilling:

```bash
python habit_tracker.py done "Read 20 pages" --date 2026-09-19
```

### 🗂️ Duplicate File Finder
A local utility that finds duplicate files by first grouping files by size and then comparing SHA-256 hashes. It streams large files in chunks instead of loading them fully into memory.

Example:

```bash
python duplicate_file_finder.py ./Downloads
```

The report groups matching files and shows how many duplicate copies were found. It only reads files; it does not delete or modify anything.

## Tests

Run all unit tests with:

```bash
python -m unittest discover -s tests
```

## Requirements

- Python 3.10+
- No third-party packages required

## Security

Projects run locally and do not require API keys. Do not commit passwords, private tokens, or other secrets.

## License

MIT License.

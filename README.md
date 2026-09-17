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

Use it to detect accidental or unexpected file changes after downloads or transfers.

### 📚 Markdown TOC Generator
A developer utility that scans Markdown headings and generates a clean table of contents with anchor links. It ignores headings inside fenced code blocks and handles duplicate heading slugs.

Examples:

```bash
python markdown_toc_generator.py README.md
python markdown_toc_generator.py README.md --max-level 2
python markdown_toc_generator.py README.md --output toc.md
```

### 🌐 URL Health Checker
A standard-library CLI tool that checks whether websites are reachable and reports HTTP status codes and response time. Multiple URLs can be checked concurrently.

Examples:

```bash
python url_health_checker.py example.com https://github.com
python url_health_checker.py example.com example.org --timeout 3 --workers 2
```

The tool returns a non-zero exit code if any URL is not reachable with a successful HTTP response.

Run tests:

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

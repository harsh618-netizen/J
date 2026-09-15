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

Run tests:

```bash
python -m unittest discover -s tests
```

## Security

Projects run locally and do not require API keys. Do not commit passwords, private tokens, or other secrets.

## License

MIT License.

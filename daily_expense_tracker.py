"""Daily Expense Tracker - a simple local-only Python CLI project."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.csv")


def add_expense(amount: float, category: str, note: str = "") -> None:
    """Append one expense record to the local CSV file."""
    file_exists = DATA_FILE.exists()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "amount", "category", "note"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"date": date.today().isoformat(), "amount": f"{amount:.2f}", "category": category, "note": note})


def load_expenses() -> list[dict[str, str]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def print_summary(expenses: list[dict[str, str]]) -> None:
    if not expenses:
        print("No expenses recorded yet.")
        return
    total = sum(float(item["amount"]) for item in expenses)
    by_category: dict[str, float] = {}
    for item in expenses:
        by_category[item["category"]] = by_category.get(item["category"], 0.0) + float(item["amount"])

    print(f"\nTotal spent: ₹{total:.2f}")
    print("By category:")
    for category, amount in sorted(by_category.items(), key=lambda pair: pair[1], reverse=True):
        print(f"- {category}: ₹{amount:.2f}")


def main() -> None:
    print("💰 Daily Expense Tracker")
    print("Type 'summary' to view totals or 'exit' to quit.\n")
    while True:
        command = input("Command (add/summary/exit): ").strip().lower()
        if command == "exit":
            print("Goodbye!")
            break
        if command == "summary":
            print_summary(load_expenses())
            continue
        if command != "add":
            print("Please choose add, summary, or exit.")
            continue

        try:
            amount = float(input("Amount (₹): ").strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            print("Enter a valid positive amount.")
            continue
        category = input("Category: ").strip() or "Other"
        note = input("Note (optional): ").strip()
        add_expense(amount, category, note)
        print("Expense saved locally.\n")


if __name__ == "__main__":
    main()

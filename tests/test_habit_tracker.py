import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from habit_tracker import add_habit, current_streak, load_data, mark_habit, save_data


class HabitTrackerTests(unittest.TestCase):
    def test_add_and_mark_habit(self):
        data = {"habits": {}}
        add_habit(data, "Read")
        mark_habit(data, "Read", "2026-09-18")
        self.assertEqual(data["habits"]["Read"]["completed"], ["2026-09-18"])

    def test_current_streak(self):
        today = date(2026, 9, 19)
        completed = [(today - timedelta(days=i)).isoformat() for i in range(3)]
        self.assertEqual(current_streak(completed, today), 3)

    def test_save_and_load(self):
        data = {"habits": {"Study": {"completed": ["2026-09-19"]}}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "habits.json"
            save_data(path, data)
            self.assertEqual(load_data(path), data)


if __name__ == "__main__":
    unittest.main()

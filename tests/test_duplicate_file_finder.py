import tempfile
import unittest
from pathlib import Path

from duplicate_file_finder import find_duplicates


class DuplicateFileFinderTests(unittest.TestCase):
    def test_finds_same_content_with_different_names(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "one.txt").write_text("same", encoding="utf-8")
            (root / "two.txt").write_text("same", encoding="utf-8")
            (root / "different.txt").write_text("other", encoding="utf-8")

            duplicates = find_duplicates(root)

            self.assertEqual(len(duplicates), 1)
            self.assertEqual(
                {path.name for path in next(iter(duplicates.values()))},
                {"one.txt", "two.txt"},
            )

    def test_ignores_unique_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "a.txt").write_text("a", encoding="utf-8")
            (root / "b.txt").write_text("b", encoding="utf-8")

            self.assertEqual(find_duplicates(root), {})


if __name__ == "__main__":
    unittest.main()

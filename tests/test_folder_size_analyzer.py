import tempfile
import unittest
from pathlib import Path

from folder_size_analyzer import folder_sizes, human_size


class FolderSizeAnalyzerTests(unittest.TestCase):
    def test_counts_nested_files_and_sorts_largest_first(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            small = root / "small"
            large = root / "large"
            (small / "nested").mkdir(parents=True)
            large.mkdir()
            (small / "a.txt").write_bytes(b"123")
            (small / "nested" / "b.txt").write_bytes(b"45")
            (large / "c.txt").write_bytes(b"123456")

            result = folder_sizes(root)

            self.assertEqual([p.name for p, _ in result], ["large", "small"])
            self.assertEqual([size for _, size in result], [6, 5])

    def test_rejects_non_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            file_path = Path(temp) / "file.txt"
            file_path.write_text("hello", encoding="utf-8")
            with self.assertRaises(NotADirectoryError):
                folder_sizes(file_path)

    def test_human_size(self):
        self.assertEqual(human_size(0), "0.0 B")
        self.assertEqual(human_size(1024), "1.0 KB")


if __name__ == "__main__":
    unittest.main()

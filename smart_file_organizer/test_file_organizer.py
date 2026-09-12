import unittest
from pathlib import Path

from file_organizer import category_for, unique_destination


class FileOrganizerTests(unittest.TestCase):
    def test_category_for_known_extension(self):
        self.assertEqual(category_for(Path("photo.PNG")), "Images")
        self.assertEqual(category_for(Path("report.pdf")), "Documents")

    def test_category_for_unknown_extension(self):
        self.assertEqual(category_for(Path("data.bin")), "Others")

    def test_unique_destination_adds_counter(self):
        self.assertEqual(unique_destination(Path("missing.txt")), Path("missing.txt"))


if __name__ == "__main__":
    unittest.main()

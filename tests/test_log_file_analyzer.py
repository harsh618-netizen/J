import unittest

from log_file_analyzer import analyze_lines


class LogAnalyzerTests(unittest.TestCase):
    def test_counts_levels_and_ips(self):
        lines = [
            "INFO request from 10.0.0.1",
            "ERROR request from 10.0.0.1",
            "WARNING retry from 10.0.0.2",
            "DEBUG health check",
        ]
        report = analyze_lines(lines)
        self.assertEqual(report["total_lines"], 4)
        self.assertEqual(report["levels"]["INFO"], 1)
        self.assertEqual(report["levels"]["ERROR"], 1)
        self.assertEqual(report["levels"]["WARNING"], 1)
        self.assertEqual(report["levels"]["DEBUG"], 1)
        self.assertEqual(report["top_ips"][0], ("10.0.0.1", 2))

    def test_unclassified_lines_are_other(self):
        report = analyze_lines(["server started successfully"])
        self.assertEqual(report["total_lines"], 1)
        self.assertEqual(report["levels"]["OTHER"], 1)
        self.assertEqual(report["top_ips"], [])


if __name__ == "__main__":
    unittest.main()

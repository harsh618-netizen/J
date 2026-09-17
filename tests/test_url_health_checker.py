import unittest
from unittest.mock import patch

from url_health_checker import check_url


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class UrlHealthCheckerTests(unittest.TestCase):
    @patch("url_health_checker.urlopen", return_value=FakeResponse())
    def test_adds_https_and_reports_up(self, mock_urlopen):
        result = check_url("example.com")
        self.assertEqual(result.status, "UP")
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.url.startswith("https://"))
        mock_urlopen.assert_called_once()

    @patch("url_health_checker.urlopen", side_effect=OSError("connection failed"))
    def test_reports_down_on_connection_error(self, mock_urlopen):
        result = check_url("https://example.com")
        self.assertEqual(result.status, "DOWN")
        self.assertIsNone(result.status_code)
        self.assertIn("connection failed", result.error)


if __name__ == "__main__":
    unittest.main()

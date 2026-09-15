import unittest

from json_toolkit import flatten_json


class TestFlattenJson(unittest.TestCase):
    def test_nested_values(self):
        data = {"user": {"name": "Harsh", "skills": ["Python", "Pandas"]}}
        self.assertEqual(
            flatten_json(data),
            {
                "user.name": "Harsh",
                "user.skills.0": "Python",
                "user.skills.1": "Pandas",
            },
        )

    def test_scalar(self):
        self.assertEqual(flatten_json({"active": True}), {"active": True})


if __name__ == "__main__":
    unittest.main()

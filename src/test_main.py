import unittest

from main import extract_markdown


class TestExtractTitle(unittest.TestCase):
    def test_func(self):
        header = "Testing function"
        new_header = extract_markdown(header, f"# {header}\n")
        self.assertEqual(header, new_header)


if __name__ == "__main__":
    unittest.main()


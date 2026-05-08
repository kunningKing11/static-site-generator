import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is a test.")
        self.assertEqual(node.to_html(), "<b>This is a test.</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "It might be problematic if this test doesn't pass...")
        self.assertEqual(node.to_html(), "<i>It might be problematic if this test doesn't pass...</i>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")

if __name__ == "__main__":
    unittest.main()


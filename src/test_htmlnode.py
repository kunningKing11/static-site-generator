import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="p", value="This is an HTML node", props={"an interesting property": "useless"})
        node2 = HTMLNode(tag="p", value="This is an HTML node", props={"an interesting property": "useless"})
        self.assertEqual(repr(node), repr(node2))

    def test_props_to_html(self):
        node = HTMLNode(tag="span", value="`span` is a piece of text", props={ "interesting property": "what is this for?" })
        expected = ' interesting property="what is this for?"'
        self.assertEqual(node.props_to_html(), expected)

if __name__ == "__main__":
    unittest.main()


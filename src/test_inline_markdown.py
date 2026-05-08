import unittest

from textnode import TextType, TextNode
from inline_markdown import text_to_textnodes, split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links


class TestSplitNodes(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(True, True)

    def test_text_to_textnodes(self):
        text = "Hi! My name is [Jeff Bezos](https://amazon.com). Click on my name to help me become a trillionaire!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Hi! My name is ", TextType.TEXT),
                TextNode(
                    "Jeff Bezos",
                    TextType.LINK,
                    "https://amazon.com",
                ),
                TextNode(". Click on my name to help me become a trillionaire!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link",
                    TextType.LINK,
                    "https://google.com",
                ),
            ],
            new_nodes,
        )

class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is text with a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()


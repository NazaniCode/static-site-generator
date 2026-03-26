import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_urlempty(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, "http://www.youtube.com")
        self.assertNotEqual(node, node2)

    def test_noteq_urldiff(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.youtube.cob")
        node2 = TextNode("This is a text node", TextType.TEXT, "http://www.youtube.com")
        self.assertNotEqual(node, node2)

    def test_noteq_typediff(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_noteq_textdiff(self):
        node = TextNode("This is a text node lol", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text_to_list_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_text_to_list_delimiter_multi(self):
        node = TextNode(
            "This is text with two `code block` `code block 2` words", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with two ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("code block 2", TextType.CODE),
                TextNode(" words", TextType.TEXT),
            ],
        )

    def test_text_to_list_delimiter_incorrect(self):
        node = TextNode(
            "This is text with incorrect `code block `code block 2` delimiters",
            TextType.TEXT,
        )
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_text_to_list_delimiter_multi_input(self):
        node = TextNode(
            "This is text with two `code block` `code block 2` words, and _italic_ word",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is a text with a **bold block** and _italic_", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with two ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("code block 2", TextType.CODE),
                TextNode(" words, and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )


if __name__ == "__main__":
    unittest.main()

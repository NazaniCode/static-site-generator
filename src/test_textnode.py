import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()

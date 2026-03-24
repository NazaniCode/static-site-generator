import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            "p", "hello world", [HTMLNode()], {"href": "https://www.google.com"}
        )
        node2 = HTMLNode(
            "p", "hello world", [HTMLNode()], {"href": "https://www.google.com"}
        )
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode(
            "div", "hello world", [HTMLNode()], {"href": "https://www.google.com"}
        )
        node2 = HTMLNode(
            "p", "hello world", [HTMLNode()], {"href": "https://www.google.com"}
        )
        self.assertNotEqual(node, node2)

    def test_proptstohtml(self):
        node = HTMLNode(
            "div",
            "hello world",
            [HTMLNode()],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        props_to_html = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(props_to_html, expected)


if __name__ == "__main__":
    unittest.main()

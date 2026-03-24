import unittest

from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_manyleafs(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_nochildren(self):
        node = ParentNode("div", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_bigeverything(self):
        child1 = LeafNode("label", "Email address:", {"for": "email"})
        child2 = LeafNode(
            "input", "", {"type": "email", "class": "form-control", "id": "email"}
        )
        parent1 = ParentNode("div", [child1, child2], {"class": "form-group"})

        child3 = LeafNode("label", "Password:", {"for": "pwd"})
        child4 = LeafNode(
            "input", "", {"type": "password", "class": "form-control", "id": "pwd"}
        )
        parent2 = ParentNode("div", [child3, child4], {"class": "form-group"})

        parent3 = LeafNode("button", "Submit", {"type": "submit"})

        grandparent = ParentNode("form", [parent1, parent2, parent3], {"role": "form"})

        self.maxDiff = None
        self.assertEqual(
            grandparent.to_html(),
            '<form role="form"><div class="form-group"><label for="email">Email address:</label><input class="form-control" id="email" type="email"></div><div class="form-group"><label for="pwd">Password:</label><input class="form-control" id="pwd" type="password"></div><button type="submit">Submit</button></form>',
        )


if __name__ == "__main__":
    unittest.main()

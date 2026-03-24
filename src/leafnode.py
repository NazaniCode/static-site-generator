from __future__ import annotations
from htmlnode import HTMLNode
from textnode import TextNode, TextType

void_elements = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
]


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"leaf node {self} does not have value")
        if self.tag is None:
            return self.value

        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            html = f"<{self.tag}"
            html += self.props_to_html()
            if self.tag in void_elements:
                html += ">"
            else:
                html += f">{self.value}</{self.tag}>"
            return html

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": "alt"})
        case _:
            raise ValueError(
                f"{text_node} TextType: {text_node.text_type} is not supported"
            )

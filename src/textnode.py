from __future__ import annotations
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        if self.text_type is TextType:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        separated = node.text.split(delimiter)
        if len(separated) % 2 == 0:
            raise ValueError(f"Markdown node {node} has invalid syntax")
        for i in range(0, len(separated)):
            if i == 0 and separated[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(separated[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(separated[i], text_type))

    return new_nodes

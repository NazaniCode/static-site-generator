from __future__ import annotations
from enum import Enum
import re


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


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def extract_markdown_images(text: str):
    images_list = []
    matches = re.findall(r"!\[([^\]]*)\]\(([^\)]+)\)", text)

    for alt, url in matches:
        images_list.append((alt, url))

    return images_list


def extract_markdown_links(text: str):
    link_list = []
    matches = re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]+)\)", text)

    for anchor, url in matches:
        link_list.append((anchor, url))

    return link_list


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


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        extracted = extract_markdown_images(text)
        if len(extracted) == 0:
            new_nodes.append(node)
            continue
        for alt, image_url in extracted:
            sections = text.split(f"![{alt}]({image_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append((TextNode(alt, TextType.IMAGE, image_url)))
            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        extracted = extract_markdown_links(text)
        if len(extracted) == 0:
            new_nodes.append(node)
            continue
        for anchor, link_url in extracted:
            sections = text.split(f"[{anchor}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append((TextNode(anchor, TextType.LINK, link_url)))
            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

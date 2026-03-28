from __future__ import annotations
from enum import Enum
import re
from leafnode import text_node_to_html_node
from textnode import text_to_textnodes, TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode


def markdown_to_html_node(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in markdown_blocks:
        html_node = text_block_to_html_node(block)
        html_nodes.append(html_node)

    parent_html = ParentNode("div", html_nodes)
    return parent_html


def text_block_to_html_node(block: str):
    block_type: BlockType = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_block_to_children(block.replace("\n", " ")))
        case BlockType.HEADING:
            heading_number = heading_block_to_heading_amount(block)
            return ParentNode(
                f"h{heading_number}",
                text_block_to_children(block[heading_number + 1 :]),
            )
        case BlockType.CODE:
            return ParentNode(
                "pre",
                [text_node_to_html_node(TextNode(block[3:-3].lstrip(), TextType.CODE))],
            )
        case BlockType.QUOTE:
            quote_pattern = r"^> ?(.+)$"
            quotes = re.findall(quote_pattern, block, re.MULTILINE)
            quote = ""
            for q in quotes:
                quote += q + " "
            quote = quote[:-1]
            return ParentNode("blockquote", text_block_to_children(quote))
        case BlockType.UNORDERED_LIST:
            ul_children = []
            unordered_item_pattern = r"^- (.+)$"
            formatted = re.findall(unordered_item_pattern, block, re.MULTILINE)
            for item in formatted:
                item = item.strip()
                ul_children.append(ParentNode("li", text_block_to_children(item)))
            return ParentNode("ul", ul_children)
        case BlockType.ORDERED_LIST:
            ol_children = []
            ordered_item_pattern = r"^\d+\. (.+)$"
            formatted = re.findall(ordered_item_pattern, block, re.MULTILINE)
            for item in formatted:
                item = item.strip()
                ol_children.append(ParentNode("li", text_block_to_children(item)))
            return ParentNode("ol", ol_children)


def text_block_to_children(block: str):
    children = []
    text_nodes = text_to_textnodes(block)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def heading_block_to_heading_amount(heading_block: str):
    heading_amount = 0
    for i in range(0, 6):
        if heading_block[i] == "#":
            heading_amount += 1
        else:
            return heading_amount
    return heading_amount


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


heading_pattern = r"^(#{1,6}) (.+)"
code_pattern = r"^```\n[\s\S]*\n```$"
unordered_pattern = r"^(- .+\n?)+$"
quote_pattern = r"^(> ?.*\n?)+$"
ordered_pattern = r"^((\d+)\. .+\n?)+$"


def block_to_block_type(block: str):
    if re.match(heading_pattern, block):
        return BlockType.HEADING
    if re.match(code_pattern, block):
        return BlockType.CODE
    if re.match(quote_pattern, block):
        return BlockType.QUOTE
    if re.match(unordered_pattern, block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def extract_title(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    if len(markdown_blocks) is 0:
        raise ValueError("markdown was empty")
    heading_block = markdown_to_blocks(markdown)[0]
    if block_to_block_type(heading_block) is not BlockType.HEADING:
        raise ValueError(
            f"Markdown {heading_block[0:10]}... did not start with a heading"
        )
    if heading_block_to_heading_amount(heading_block) > 1:
        raise ValueError(
            f"Markdown {heading_block[0:10]}... started with a header but not an h1"
        )
    return heading_block[2:].strip()


def is_ordered_list(text):
    if not re.match(ordered_pattern, text):
        return False
    numbers = [int(n) for n in re.findall(r"^(\d+)\.", text, re.MULTILINE)]
    return numbers == list(range(1, len(numbers) + 1))


def markdown_to_blocks(markdown: str):
    blocks = []

    formatted_markdown = markdown.strip()
    for block in formatted_markdown.split("\n\n"):
        block.strip()
        if block == "" or block == "\n":
            continue
        blocks.append(block)

    return blocks

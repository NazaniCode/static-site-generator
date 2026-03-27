from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


heading_pattern = r"^(#{1,6}) (.+)"
code_pattern = r"^```\n[\s\S]*\n```$"
quote_pattern = r"^(> ?.+\n?)+$"
unordered_pattern = r"^(- .+\n?)+$"
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

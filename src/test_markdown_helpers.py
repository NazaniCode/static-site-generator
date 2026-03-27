import unittest

from markdown_helpers import block_to_block_type, markdown_to_blocks, BlockType


class TestMarkdownHelpers(unittest.TestCase):
    def test_block_to_block_type(self):
        tests = [
            "# H1 Heading",
            "## H2 Heading",
            "###### H6 Heading",
            "####### Not a heading (7 hashes)",
            "#No space, not a heading",
            "Not a heading at all",
            "```\nsome code\nmore code\n```",  # ✅
            "```\n\n```",  # ✅ empty code block
            "```some code```",  # ❌ no newlines
            "``\nsome code\n``",  # ❌ only 2 backticks
            "> Hello",  # ✅
            ">Hello",  # ✅ no space is allowed
            "> Line one\n> Line two",  # ✅ multiline
            "Hello",  # ❌ no >
            "> Line one\nNot a quote",  # ❌ second line missing >
            "- item one",  # ✅
            "- item one\n- item two",  # ✅ multiline
            "-item one",  # ❌ missing space
            "- item one\nitem two",  # ❌ second line missing -
            "* item one",  # ❌ wrong character
            "1. item one",  # ✅
            "1. item one\n2. item two\n3. item three",  # ✅
            "1. item one\n3. item three",  # ❌ skips 2
            "2. item one\n3. item two",  # ❌ doesn't start at 1
            "1. item one\n2. item two\n2. item two",  # ❌ repeats 2
            "1.item one",  # ❌ missing space
        ]

        matches = []
        for test in tests:
            matches.append(block_to_block_type(test))

        self.assertEqual(
            matches,
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.UNORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.ORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_markdown_to_blocks_one_element(self):
        md = """
- this is a list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- this is a list item"],
        )

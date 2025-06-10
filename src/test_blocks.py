from blocks import markdown_to_blocks, block_to_block_type, BlockType
import unittest


class TestTextNode(unittest.TestCase):
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


class TestBlockClassification(unittest.TestCase):
    def test_heading(self):
        md = """# This is an heading"""

        self.assertEqual(block_to_block_type(md), (BlockType.Heading, "#"))

    def test_heading_middle(self):
        md = """this is a test # This is an heading"""

        self.assertEqual(block_to_block_type(md), (BlockType.Paragraph, ""))

    def test_heading_special_char(self):
        md = """# -This is an heading"""
        self.assertEqual(block_to_block_type(md), (BlockType.Heading, "#"))

    def test_code_block(self):
        md = r"""```
def main():
    print("Hello world")
```"""

        self.assertEqual(block_to_block_type(md), (BlockType.Code, ""))

    def test_order_list(self):
        md = r"""1. This is item
2. This is another item"""

        self.assertEqual(block_to_block_type(md), (BlockType.OrderedList, ""))

    def test_order_fail_whitespace(self):
        md = r"""1. This is item
2.This is another item"""

        self.assertEqual(block_to_block_type(md), (BlockType.Paragraph, ""))

    def test_order(self):
        md = r"""1. This is item
3. This is another item"""

        self.assertEqual(block_to_block_type(md), (BlockType.Paragraph, ""))

    def test_unordered(self):
        md = r"""- This is item
- This is another item"""

        self.assertEqual(block_to_block_type(md), (BlockType.UnorderedList, ""))

    def test_fail_whitespace_unordered(self):
        md = r"""- This is item
-This is another item"""

        self.assertEqual(block_to_block_type(md), (BlockType.Paragraph, ""))

from enum import Enum
import re


class BlockType(Enum):
    Paragraph = "paragraph"
    Heading = "heading"
    Code = "code"
    Quote = "quote"
    UnorderedList = "unordered_list"
    OrderedList = "ordered_list"


def markdown_to_blocks(markdown: str):
    lines = markdown.split("\n\n")
    return list(filter(lambda x: x != "", map(lambda x: x.strip(), lines)))


def examine_lines(lines: list[str], pattern: str) -> bool:
    for line in lines:
        if not re.findall(pattern, line):
            return False
    return True


def examine_ordered_list(lines: list[str]):
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            return False
    return True


def block_to_block_type(block: str):
    if match := re.match(r"^(#{1,6})\s", block):
        return (BlockType.Heading, match.group(1))

    lines = block.split("\n")
    if lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.Code, ""

    if examine_lines(lines, r"^>"):
        return BlockType.Quote, ""
    if examine_lines(lines, r"^- "):
        return BlockType.UnorderedList, ""
    if examine_ordered_list(lines):
        return BlockType.OrderedList, ""

    return BlockType.Paragraph, ""

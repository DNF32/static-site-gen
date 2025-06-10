from blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode
from text_splitter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
import re


type Markdown = str


def clean_code_block(block: str) -> str:
    lines = block.split("\n")
    clean_lines = lines[1:-1]
    return "\n".join(clean_lines) + "\n"


def clean_paragraph_block(block: str) -> str:
    lines = block.split("\n")
    return " ".join(lines)


def clean_quote_block(block: str) -> str:
    lines = block.split("\n")
    return "\n".join(map(lambda x: x.lstrip("> "), lines))


def clean_ordered_line(line: str) -> str:
    match = re.match(r"^\d+\. (.*)", line)
    if match:
        remaining = match.group(1)
        return remaining
    else:
        return ""


def clean_unordered_line(line: str) -> str:
    match = re.match(r"^\* (.*)", line)
    if match:
        remaining = match.group(1)
        return remaining
    else:
        return ""


def markdown_to_html_node(markdown: Markdown):
    # Create root <div> container
    root = ParentNode("div")
    root.children = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type, info = block_to_block_type(block)
        match block_type:
            case BlockType.Heading:
                node_block = ParentNode(f"h{info}")
                text_nodes = text_to_textnodes(block.lstrip(info + " "))
                node_block.children = list(map(text_node_to_html_node, text_nodes))
            case BlockType.Code:
                node_block = ParentNode("pre")
                code_node_block = ParentNode("code")
                node_block.children = [code_node_block]

                code_node_block.children = [
                    text_node_to_html_node(
                        TextNode(clean_code_block(block), TextType.Text)
                    )
                ]
            case BlockType.Quote:
                clean_block = clean_quote_block(block)

                node_block = ParentNode("blockquote")
                text_nodes = text_to_textnodes(clean_block)
                node_block.children = list(map(text_node_to_html_node, text_nodes))

            case BlockType.OrderedList:
                node_block = ParentNode("ol")
                node_block.children = []

                for line in block.split("\n"):
                    parent_line = ParentNode("li")
                    node_block.children.append(parent_line)

                    line = clean_ordered_line(line)
                    text_nodes = text_to_textnodes(line)
                    parent_line.children = list(map(text_node_to_html_node, text_nodes))

            case BlockType.UnorderedList:
                node_block = ParentNode("ul")
                node_block.children = []

                for line in block.split("\n"):
                    parent_line = ParentNode("li")
                    node_block.children.append(parent_line)

                    line = clean_unordered_line(line)
                    text_nodes = text_to_textnodes(line)
                    parent_line.children = list(map(text_node_to_html_node, text_nodes))

            case BlockType.Paragraph:
                node_block = ParentNode("p")
                clean_block = clean_paragraph_block(block)

                text_nodes = text_to_textnodes(clean_block)
                node_block.children = list(map(text_node_to_html_node, text_nodes))

            case _:
                Exception("Non Valid  BlockType")

        root.children.append(node_block)
    return root

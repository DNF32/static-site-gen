from collections.abc import Callable
from textnode import TextType, TextNode
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.Text:
            new_nodes.append(old_node)
            continue
        split = old_node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise Exception("Invalid markdown")
        for i in range(len(split)):
            match i % 2:
                case 0:
                    new_nodes.append(TextNode(split[i], TextType.Text))
                case 1:
                    new_nodes.append(TextNode(split[i], text_type))

    return new_nodes


def split_nodes_tag(
    old_nodes: list[TextNode],
    tag_finder: Callable[[str], list[tuple[str, str]]],
    formatter: Callable[[str, str], str],
    text_type: TextType,
):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.Text:
            new_nodes.append(old_node)
            continue
        tags_found = tag_finder(old_node.text)
        current_text = old_node.text
        for tag in tags_found:
            parts = current_text.split(formatter(tag[0], tag[1]), maxsplit=1)
            new_nodes.append(TextNode(parts[0], TextType.Text))
            new_nodes.append(TextNode(tag[0], text_type=text_type, url=tag[1]))

            current_text = parts[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.Text))
    return new_nodes


def image_match_formatter(alt_text: str, link: str):
    return f"![{alt_text}]({link})"


def link_match_formatter(anchor_text: str, link: str):
    return f"[{anchor_text}]({link})"


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<=\!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_images(old_nodes: list[TextNode]):
    return split_nodes_tag(
        old_nodes, extract_markdown_images, image_match_formatter, TextType.Image
    )


def split_nodes_links(old_nodes: list[TextNode]):
    return split_nodes_tag(
        old_nodes, extract_markdown_links, link_match_formatter, TextType.Links
    )


####################################
def text_to_textnodes(text: str):
    node = TextNode(text, TextType.Text)

    nodes = split_nodes_images([node])
    nodes = split_nodes_links(nodes)

    nodes = split_nodes_delimiter(nodes, "`", TextType.Code)
    nodes = split_nodes_delimiter(nodes, "**", TextType.Bold)
    nodes = split_nodes_delimiter(nodes, "_", TextType.Italic)

    return nodes

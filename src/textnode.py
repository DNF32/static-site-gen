from enum import Enum
from typing import Optional

from htmlnode import LeafNode


class TextType(Enum):
    Bold = "bold"
    Italic = "italic"
    Code = "code"
    Links = "links"
    Image = "images"
    Text = "text"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.Text:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.Bold:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.Italic:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.Code:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.Links:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.Image:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("TextType invalid")

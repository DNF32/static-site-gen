from __future__ import annotations
from typing import Optional, Sequence


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[Sequence[HTMLNode]] = None,
        props: Optional[dict] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        repr = ""
        if self.props is None:
            return ""
        for key, value in self.props.items():
            repr += f'{key}="{value}" '
        return repr.rstrip()

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: str, props: Optional[dict] = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        match (self.props, self.tag):
            case (None, None):
                return f"{self.value}"
            case (None, tag) if tag is not None:
                return f"<{tag}>{self.value}</{tag}>"
            case (props, tag):
                return f"<{tag} {self.props_to_html()}>{self.value}</{tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Optional[Sequence[HTMLNode]] = None,
        props: Optional[dict] = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        if self.children is None:
            raise ValueError("Children is missing")
        parent = f"<{self.tag}>"
        for child in self.children:
            parent += f"{child.to_html()}"
        return f"{parent}</{self.tag}>"

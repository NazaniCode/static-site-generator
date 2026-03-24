from __future__ import annotations

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"{self} does not contain value")

        if self.children is None:
            raise ValueError(f"{self} does not contain children")

        html = f"<{self.tag}"
        html += self.props_to_html()
        html += ">"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"

        return html

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props}"

from __future__ import (
    annotations,
)  # if this is not imported, the children type in the __init__ will throw a type error
from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str = "",
        children: list[HTMLNode] = [],
        attrs: dict[str, str] = {},
    ):
        self.tag: str | None = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.attrs: dict[str, str] = attrs

    def add_child(self, child: HTMLNode):
        self.children.append(child)

    def to_html(self) -> str:
        children = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.attrs_to_html()}>{self.value}{children}</{self.tag}>"

    def attrs_to_html(self) -> str:
        _attrs: str = ""

        if self.attrs is not None:
            for k, v in self.attrs.items():
                _attrs += f' {k}="{v}"'

        return _attrs

    @override
    def __repr__(self) -> str:
        return f"tag = {self.tag}\n value = {self.value}\n, children = {self.children}\n, attrs = {self.attrs_to_html()}\n)"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode],
        attrs: dict[str, str] | None = None,
    ):
        if tag is None or tag == "":
            raise ValueError("HTML tag from a parentnode cannot be None or empty")
        if children is None or children == []:
            raise ValueError("children from a parentnode cannot be None or empty")

        super().__init__(tag, None, children, attrs)

    def add_child(self, child: HTMLNode):
        self.children.append(child)

    @override
    def to_html(self) -> str:
        if self.tag is None or self.tag == "":
            raise ValueError("HTML tag from a parentnode cannot be None or empty")
        if self.children is None or self.children == []:
            raise ValueError("children from a parentnode cannot be None or empty")

        children = "".join([child.to_html() for child in self.children])
        html = ""
        if self.tag == "code":
            html = (
                f"<pre><{self.tag}{self.attrs_to_html()}>{children}</{self.tag}></pre>"
            )
        else:
            html = f"<{self.tag}{self.attrs_to_html()}>{children}</{self.tag}>"

        return html


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        attrs: dict[str, str] | None = None,
    ):
        if value is None:
            raise ValueError("LeafNode value cannot be None")

        super().__init__(tag, value, None, attrs)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")

        if self.tag is None or self.tag == "":
            return self.value

        html = ""
        if self.tag == "code":
            html = f"<pre><{self.tag}{self.attrs_to_html()}>{self.value}</{self.tag}></pre>"
        else:
            html = f"<{self.tag}{self.attrs_to_html()}>{self.value}</{self.tag}>"

        return html

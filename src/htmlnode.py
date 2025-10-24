from __future__ import (
    annotations,
)  # if this is not imported, the children type in the __init__ will throw a type error
from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str = "",
        children: list[HTMLNode] | None = None,
        attrs: dict[str, str] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str = value
        self.children: list[HTMLNode] | None = children
        self.attrs: dict[str, str] | None = attrs

    def add_child(self, child: HTMLNode):
        if self.children is None:
            self.children = []
        self.children.append(child)

    def to_html(self) -> str:
        children = "".join([child.to_html() for child in (self.children or [])])
        if children == "" and self.value == "":
            return ""

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
        children: list[HTMLNode] | None = None,
        attrs: dict[str, str] | None = None,
    ):
        if tag is None or tag == "":
            raise ValueError("HTML tag from a parentnode cannot be None or empty")
        if children == [] or children is None:
            raise ValueError("children from a parentnode cannot be None or empty")

        super().__init__(tag, "", children, attrs)

    @override
    def add_child(self, child: HTMLNode):
        if self.children is None:
            self.children: list[HTMLNode] | None = []
        self.children.append(child)

    @override
    def to_html(self) -> str:
        if self.tag is None or self.tag == "":
            raise ValueError("HTML tag from a parentnode cannot be None or empty")
        if self.children == []:
            raise ValueError("children from a parentnode cannot be None or empty")

        children = "".join([child.to_html() for child in (self.children or [])])
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
        value: str = "",
        attrs: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, [], attrs)

    @override
    def to_html(self) -> str:
        if self.tag is None or self.tag == "":
            return self.value

        html = ""
        if self.tag == "code":
            html = f"<pre><{self.tag}{self.attrs_to_html()}>{self.value}</{self.tag}></pre>"
        else:
            html = f"<{self.tag}{self.attrs_to_html()}>{self.value}</{self.tag}>"

        return html

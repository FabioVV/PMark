from __future__ import (
    annotations,
)  # if this is not imported, the children type in the __init__ will throw a type error]
from typing import override
from textnode import TextNode, TextType


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        attrs: dict[str, str] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.attrs: dict[str, str] | None = attrs

    def to_html(self) -> str:
        raise NotImplementedError

    def attrs_to_html(self) -> str:
        _attrs: str = ""

        if self.attrs is not None:
            for k, v in self.attrs.items():
                _attrs += f' {k}="{v}"'

        return _attrs

    @override
    def __repr__(self) -> str:
        return f"tag = {self.tag}\n value = {self.value}\n, children = {self.children}\n, attrs = {self.attrs_to_html()}\n)"

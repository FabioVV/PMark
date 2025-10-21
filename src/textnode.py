from enum import Enum
from typing import override


class TextType(Enum):
    PLAIN_TEXT = "PLAIN_TEXT"
    BOLD_TEXT = "BOLD_TEXT"
    ITALIC_TEXT = "ITALIC_TEXT"
    UNDERLINE_TEXT = "UNDERLINE_TEXT"
    CODE_TEXT = "CODE_TEXT"
    LINK_TEXT = "LINK_TEXT"
    IMAGE_TEXT = "IMAGE_TEXT"
    STRIKETHROUGH_TEXT = "STRIKETHROUGH_TEXT"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False

        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    @override
    def __repr__(self) -> str:
        return (
            f"text=({self.text})\n type=({self.text_type.value})\n url=({self.url})\n"
        )

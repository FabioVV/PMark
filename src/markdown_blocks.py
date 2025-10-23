from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"
    CODE = "code"
    QUOTE = "quote"


def block_to_block_type(md_text: str) -> BlockType:
    md_text = md_text.strip()  # just for safety
    if (
        md_text.startswith("# ")
        or md_text.startswith("## ")
        or md_text.startswith("### ")
        or md_text.startswith("#### ")
        or md_text.startswith("##### ")
        or md_text.startswith("###### ")
    ):
        return BlockType.HEADING
    elif md_text.startswith("* ") or md_text.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif md_text.startswith("1. "):
        _m = md_text.split("\n")

        for i, li in enumerate(_m):
            if i + 1 != int(li[0]):
                return BlockType.PARAGRAPH

        return BlockType.ORDERED_LIST
    elif md_text.startswith(">"):
        return BlockType.QUOTE
    elif md_text.startswith("```") and md_text.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH

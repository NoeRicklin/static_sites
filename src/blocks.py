from enum import Enum
from functools import reduce
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD_LIST = "unordered_list"
    ORD_LIST = "ordered_list"


def block_to_block_type(block):
    if re.fullmatch("^#{1,6} .*$", block):
        return BlockType.HEADING
    if re.match("^```.*```$", block):
        return BlockType.CODE
    lines = block.split("\n")
    if reduce(lambda x,y: x and y[0] == ">", lines, True):
        return BlockType.QUOTE
    if reduce(lambda x,y: x and re.match("^[*-] .*$", y), lines, True):
        return BlockType.UNORD_LIST
    if (cur_num := lines[0][0]).isdigit():
        for line in lines:
            if not re.match(f"^{cur_num}. .*$", line):
                break
            cur_num = str(int(cur_num) + 1)
        else:
            return BlockType.ORD_LIST
    return BlockType.PARAGRAPH


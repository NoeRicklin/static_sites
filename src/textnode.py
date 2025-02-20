from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for node in old_nodes:
        text = node.text
        text_blocks = text.split(delimiter)
        if text_blocks[-1] == "":
            text_blocks.pop()
        for index, text_block in enumerate(text_blocks):
            if index % 2 == 0:
                split_nodes.append(TextNode(text_block, node.text_type))
            else:
                split_nodes.append(TextNode(text_block, text_type))
    return split_nodes


def text_node_to_html_node(text_node):
    value = text_node.text
    tag = None
    props = None

    match text_node.text_type:
        case TextType.NORMAL:
            pass  
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props = { "href": text_node.url }
        case TextType.IMAGE:
            value = ""
            tag = "img"
            props = { "src": text_node.url, "alt": text_node.text }
        case _:
            raise ValueError("Invalid Text Type")

    leaf_node = LeafNode(tag, value, props)
    return leaf_node.to_html()


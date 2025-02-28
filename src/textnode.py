from enum import Enum
from htmlnode import LeafNode, ParentNode
from functools import reduce
from blocks import block_to_block_type, BlockType
import os
import re

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


def split_nodes_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        text = node.text
        img_extracts = extract_markdown_images(text)
        for img_extract in img_extracts:
            split = text.split(f"![{img_extract[0]}]({img_extract[1]})", maxsplit=1)
            if split[0] != "":
                split_nodes.append(TextNode(split[0], node.text_type))
            split_nodes.append(TextNode(img_extract[0], TextType.IMAGE, img_extract[1]))
            text = split[1]
        if text != "":
            split_nodes.append(TextNode(text, node.text_type, node.url))

    return split_nodes


def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        text = node.text
        link_extracts = extract_markdown_links(text)
        for link_extract in link_extracts:
            split = re.split("(?<!!)" + re.escape(f"[{link_extract[0]}]({link_extract[1]})"), text, maxsplit=1)
            if split[0] != "":
                split_nodes.append(TextNode(split[0], node.text_type))
            split_nodes.append(TextNode(link_extract[0], TextType.LINK, link_extract[1]))
            text = split[1]
        if text != "":
            split_nodes.append(TextNode(text, node.text_type, node.url))

    return split_nodes


def text_to_textnodes(text):
    rootnode = TextNode(text, TextType.NORMAL)
    delimiter_splits = split_nodes_delimiter([rootnode], "**", TextType.BOLD)
    delimiter_splits = split_nodes_delimiter(delimiter_splits, "*", TextType.ITALIC)
    delimiter_splits = split_nodes_delimiter(delimiter_splits, "`", TextType.CODE)
    all_splits = split_nodes_image(split_nodes_link(delimiter_splits))

    return all_splits


def text_node_to_html_node(text_node):
    leaf_node = text_node_to_leaf_node(text_node)
    return leaf_node.to_html()


def text_node_to_leaf_node(text_node):
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
    return leaf_node


def extract_markdown_images(text):
    regex_pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex_pattern, text)
    return matches


def extract_markdown_links(text):
    regex_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex_pattern, text)
    return matches

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block for block in blocks if block != ""]

def block_to_html_node(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block)
            html_leaf_nodes = list(map(lambda x: text_node_to_leaf_node(x), text_nodes))
            block_node = ParentNode("p", html_leaf_nodes)
            return block_node
        case BlockType.HEADING:
            header_level = 0
            while block[header_level] == "#":
                header_level += 1
            block = block[header_level+1:]
            text_nodes = text_to_textnodes(block)
            html_leaf_nodes = list(map(lambda x: text_node_to_leaf_node(x), text_nodes))
            block_node = ParentNode(f"h{header_level}", html_leaf_nodes)
            return block_node
        case BlockType.UNORD_LIST:
            line_nodes = []
            for line in block.split("\n"):
                text_nodes = text_to_textnodes(line[2:])
                leaf_nodes = list(map(lambda x: text_node_to_leaf_node(x), text_nodes))
                line_nodes.append(ParentNode("li", leaf_nodes))
            block_node = ParentNode("ul", line_nodes)
            return block_node
        case BlockType.ORD_LIST:
            line_nodes = []
            for line in block.split("\n"):
                text_nodes = text_to_textnodes(line[3:])
                leaf_nodes = list(map(lambda x: text_node_to_leaf_node(x), text_nodes))
                line_nodes.append(ParentNode("li", leaf_nodes))
            block_node = ParentNode("ol", line_nodes)
            return block_node
        case BlockType.QUOTE:
            quote = ""
            for line in block.split("\n"):
                quote += line[2:]

            block_node = LeafNode("blockquote", quote)
            return block_node
        case BlockType.CODE:
            code = block[3:-3]
            block_node = LeafNode("code", code)
            return block_node
        case _:
            raise Exception("Invalid Block")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)


def extract_title(markdown):
    if (title := markdown.split("\n")[0])[0:2] != "# ":
        raise Exception("invalid markdown")
    return title[2:]


def generate_page(from_path, template_path, dest_path, basepath):
    if not (os.path.exists(from_path) and os.path.exists(template_path)):
        raise Exception("invalid path")
    markdown_file = open(from_path)
    markdown = markdown_file.read()
    template_file = open(template_path)
    template = template_file.read()
    with open(dest_path, "w") as dest:
        title = extract_title(markdown)
        html_str = markdown_to_html_node(markdown).to_html()
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html_str)
        template = template.replace('href="/', f'href="{basepath}')
        template = template.replace('src="/', f'src="{basepath}')
        dest.write(template)
    markdown_file.close()
    template_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for path in os.listdir(basepath + "/" + dir_path_content):
        if os.path.isfile(basepath + "/" + dir_path_content + "/" + path):
            new_file_name = path.rstrip(".md") + ".html"
            generate_page(basepath + "/" + dir_path_content + "/" + path, basepath + "/" + template_path, basepath + "/" + dest_dir_path + "/" + new_file_name, basepath)
        else:
            os.mkdir(basepath + "/" + dest_dir_path + "/" + path)
            generate_pages_recursive(basepath + "/" + dir_path_content + "/" + path, basepath + "/" + template_path, basepath + "/" + dest_dir_path + "/" + path, basepath)


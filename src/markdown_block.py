import re
from enum import Enum
import re

from src.htmlnode import LeafNode, HTMLNode, ParentNode
from src.markdown_inline import text_to_textnodes
from src.textnode import TextNode, text_node_to_html_node


class BLOCK_TYPE(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_lIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match("^#{1,6} ", block):
        return BLOCK_TYPE.HEADING
    if re.match("(^`{3})[\s\S]*(`{3}$)", block):
        return BLOCK_TYPE.CODE
    if re.match("^> ", block):
        return BLOCK_TYPE.QUOTE
    pattern = "^[*-] .*\n{0,1}"
    type = BLOCK_TYPE.UNORDERED_lIST
    if not re.match(pattern, block):
        pattern = "^[\d]*\..*\n{0,1}"
        type = BLOCK_TYPE.ORDERED_LIST
        if not re.match(pattern, block):
            return BLOCK_TYPE.PARAGRAPH

    for line in block.split("\n"):
        if not re.match(pattern, line):
            return BLOCK_TYPE.PARAGRAPH

    return type

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    block = ""
    new_blocks = []
    for line in lines:
        line = line.strip()
        if line != "":
            block += line + "\n"
        else:
            if block != "":
                new_blocks.append(block.removesuffix("\n"))
            block = ""

    if block != "":
        new_blocks.append(block.removesuffix("\n"))
    return new_blocks

def text_to_children(txt):
    nodes = text_to_textnodes(txt)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BLOCK_TYPE.HEADING:
                heading_number = block.count("#", 0, 5)
                children.append(ParentNode(None, text_to_children(re.split("^#{1,6} ", block)[1]), f"h{heading_number}"))
            case BLOCK_TYPE.QUOTE:
                children.append(ParentNode(None, text_to_children(re.split("^> ", block)[1]), "blockquote"))
            case BLOCK_TYPE.CODE:
                children.append(
                    ParentNode(None, [ParentNode(
                        None, text_to_children(re.split("```", block)[1]), "pre"
                        )], "code")
                )
            case BLOCK_TYPE.ORDERED_LIST:
                lists = []
                for line in block.split("\n"):
                    lists.append(ParentNode(
                        None, text_to_children(re.split("^\d\. ", line)[1]), "li")
                    )
                children.append(ParentNode(None, lists, "ol"))
            case BLOCK_TYPE.UNORDERED_lIST:
                lists = []
                for line in block.split("\n"):
                    lists.append(ParentNode(
                        None, text_to_children(re.split("^[*-] ", line)[1]), "li")
                    )
                children.append(ParentNode(None, lists, "ul"))
            case BLOCK_TYPE.PARAGRAPH:
                children.append(ParentNode(None, text_to_children(block), "p"))

    return ParentNode(None, children, "div")


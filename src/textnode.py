from enum import Enum
from src.htmlnode import LeafNode, ParentNode, HTMLNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text != other.text or
                self.text_type != other.text_type or
                self.url != other.url):
            return False

        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


class TEXT_TYPE(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


def text_node_to_html_node(text_node):
    html_node = HTMLNode(None, text_node.text, None, None)
    text_type = text_node.text_type[0]
    while text_type == TEXT_TYPE.TEXT.value and len(text_node.text_type) > 1:
        text_node.text_type = text_node.text_type[1:]
        text_type = text_node.text_type[0]

    if len(text_node.text_type) > 1:
        text_node.text_type = text_node.text_type[1:]
        html_node = ParentNode(None, [text_node_to_html_node(text_node)])
    else:
        html_node = LeafNode(None, None, text_node.text)

    match text_type:
        case TEXT_TYPE.TEXT.value:
            pass
        case TEXT_TYPE.BOLD.value:
            html_node.tag = "b"
        case TEXT_TYPE.ITALIC.value:
            html_node.tag = "i"
        case TEXT_TYPE.CODE.value:
            html_node.tag = "code"
        case TEXT_TYPE.LINK.value:
            html_node.tag = "a"
            html_node.props = {"href": text_node.url}
        case TEXT_TYPE.IMAGE.value:
            html_node.tag = "img"
            html_node.props = {"src": text_node.url, "alt": text_node.text}
            html_node.value = ""
        case _:
            raise Exception("text type is invalid")
    return html_node

import itertools
import re

from src.textnode import TextNode, TEXT_TYPE


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # document: https://docs.python.org/3/library/itertools.html#itertools.chain
    nodes = list(
        itertools.chain.from_iterable(
            map(
                lambda node: exec('raise Exception(\"Closing delimiter required\")')
                if node.text.count(delimiter) % 2 != 0
                else list(map(
                    lambda v:
                    TextNode(v[1], node.text_type, node.url) if v[0] % 2 == 0
                    else TextNode(v[1], node.text_type + [text_type], node.url),
                    enumerate(node.text.split(delimiter))
                )),
                old_nodes)
        )
    )
    return nodes


def split_nodes(extract):
    split_prefix = ""
    text_type = ""
    match extract.__name__:
        case "extract_markdown_images":
            split_prefix = "!["
            text_type = TEXT_TYPE.IMAGE.value
        case "extract_markdown_links":
            split_prefix = "["
            text_type = TEXT_TYPE.LINK.value

    def splits(nodes):
        split_nodes = []
        for node in nodes:
            extractions = extract(node.text)
            for split in extractions:
                texts_split = node.text.split(f"{split_prefix}{split[0]}]({split[1]})", 1)
                node.text = texts_split[1]
                if texts_split[0] != "":
                    split_nodes.append(TextNode(texts_split[0], node.text_type))
                split_nodes.append(TextNode(split[0], [text_type], split[1]))

            if node.text != "":
                split_nodes.append(node)
        return split_nodes

    return splits

def text_to_textnodes(text):
    nodes = [TextNode(text, [TEXT_TYPE.TEXT.value])]

    nodes = split_nodes_delimiter(nodes, "**", TEXT_TYPE.BOLD.value)
    nodes = split_nodes_delimiter(nodes, "*", TEXT_TYPE.ITALIC.value)
    nodes = split_nodes_delimiter(nodes, "`", TEXT_TYPE.CODE.value)
    nodes = split_nodes(extract_markdown_images)(nodes)
    nodes = split_nodes(extract_markdown_links)(nodes)
    return nodes
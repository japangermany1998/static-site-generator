import unittest

from src.markdown_inline import extract_markdown_links, split_nodes_delimiter, split_nodes, text_to_textnodes
from src.textnode import TextNode, text_node_to_html_node, TEXT_TYPE


class TestMarkdownInline(unittest.TestCase):
    def test_extract_markdown(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_links(text))

        text = "This is text with and ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(text.split("and", 1))

    def test_split_nodes_delimiter(self):
        node1 = TextNode("This is a `bold node`", ["bold"], "https://www.boot.dev")
        node2 = TextNode("This is a `image node`", ["image"], "https://www.boot.dev")

        print("\n".join(map(
            lambda x: text_node_to_html_node(x).to_html(),
            split_nodes_delimiter([node1, node2], "`", TEXT_TYPE.CODE.value)
        )))

    def test_split_node_images(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) aa",
            TEXT_TYPE.TEXT.value,
        )
        print(split_nodes(extract_markdown_links)([node]))

    def test_text_to_textnode(self):
        txt = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual([
            TextNode("This is ", [TEXT_TYPE.TEXT.value]),
            TextNode("text", [TEXT_TYPE.TEXT.value, TEXT_TYPE.BOLD.value]),
            TextNode(" with an ", [TEXT_TYPE.TEXT.value]),
            TextNode("italic", [TEXT_TYPE.TEXT.value, TEXT_TYPE.ITALIC.value]),
            TextNode(" word and a ", [TEXT_TYPE.TEXT.value]),
            TextNode("code block", [TEXT_TYPE.TEXT.value, TEXT_TYPE.CODE.value]),
            TextNode(" and an ", [TEXT_TYPE.TEXT.value]),
            TextNode("obi wan image", [TEXT_TYPE.IMAGE.value], "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", [TEXT_TYPE.TEXT.value]),
            TextNode("link", [TEXT_TYPE.LINK.value], "https://boot.dev"),
        ], text_to_textnodes(txt))

if __name__ == '__main__':
    unittest.main()

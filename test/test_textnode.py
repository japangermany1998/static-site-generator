import unittest

from src.htmlnode import LeafNode, ParentNode
from src.textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", ["bold"])
        node2 = TextNode("This is a text node", ["bold"])
        self.assertEqual(node, node2)
        node = TextNode("This is a text node1", ["bold1"])
        node2 = TextNode("This is a text node2", ["bold2"])
        self.assertNotEqual(node, node2)

    def test_to_html_node(self):
        node0 = TextNode("text", ["italic"])
        node1 = TextNode(f"This is a {text_node_to_html_node(node0).to_html()} node", ["bold"])
        self.assertEqual(text_node_to_html_node(node1), LeafNode("b", None, "This is a <i>text</i> node"))

        node2 = TextNode("This is link", ["link", "italic"], "https://google.com")
        expected = ParentNode(
            {"href": "https://google.com"},
            [LeafNode("i", None, "This is link")],
            "a")
        self.assertEqual(text_node_to_html_node(node2), expected)

        # node3 = TextNode("This is image", ["image"], "https://link_image.com")
        # self.assertEqual(text_node_to_html_node(node3), ParentNode({
        #     "src": "https://link_image.com", "alt": "This is image"}, None, "img"))




if __name__ == "__main__":
    unittest.main()

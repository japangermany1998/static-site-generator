import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node(self):
        node1 = HTMLNode("p", "heading", None, {"onclick": "alert(1)", "style": "color: true"})
        self.assertEqual(node1.props_to_html(), " onclick=\"alert(1)\" style=\"color: true\"")  # add assertion here

        self.assertEqual(node1.__str__(),
            "HTMLNode(Tag: p, Value: heading, Children: None, Props:{'onclick': 'alert(1)', 'style': 'color: true'})")

    def test_leaf_node(self):
        node1 = LeafNode("b", {"href": "https://www.google.com"}, "Bold text")
        self.assertEqual(node1.to_html(), "<b href=\"https://www.google.com\">Bold text</b>")

    def test_parent_node(self):
        node1 = ParentNode({"href": "https://www.google.com"}, [
            ParentNode({"href": "https://www.google.com"},[
                LeafNode("c1", {"href": "https://www.techmaster.com"}, "1"),
                LeafNode("c2", {"href": "https://www.techmaster.com"}, "2")
            ],"b1"),
            ParentNode({"href": "https://www.google.com"},[
                LeafNode("c3", {"href": "https://www.techmaster.com"}, "3"),
                LeafNode("c4", {"href": "https://www.techmaster.com"}, "4")
            ],"b2"),
        ], "a")
        print(node1.to_html())

if __name__ == '__main__':
    unittest.main()

import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("a", TextType.BOLD, "https/dummy-site.org")
        node2 = TextNode("a", TextType.BOLD, "https/dummy-site.org")
        self.assertEqual(node, node2)

    def test_eq3(self):
        text_node = TextNode("this is bold", TextType.BOLD)
        conv_text = text_node_to_html_node(text_node)
        html_repr = "<b>this is bold</b>"
        self.assertEqual(conv_text, html_repr)

    def test_eq4(self):
        text_node = TextNode("link", TextType.LINK, "https/site.com")
        conv_text = text_node_to_html_node(text_node)
        html_repr = '<a href="https/site.com">link</a>'
        self.assertEqual(conv_text, html_repr)

    def test_eq5(self):
        text_node = TextNode("image", TextType.IMAGE, "https/image.com")
        conv_text = text_node_to_html_node(text_node)
        html_repr = '<img src="https/image.com" alt="image"></img>'
        self.assertEqual(conv_text, html_repr)
    
    def test_eq6(self):
        text_node = TextNode("This is **text**, that *has* different `types`", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        correct_split_nodes = [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(", that *has* different `types`", TextType.NORMAL)
            ]
        self.assertEqual(split_nodes, correct_split_nodes)

    def test_eq7(self):
        text_node = TextNode("This is **text**, that *has* different `types`", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        correct_split_nodes = [
                TextNode("This is **text**, that *has* different ", TextType.NORMAL),
                TextNode("types", TextType.CODE)
            ]
        self.assertEqual(split_nodes, correct_split_nodes)

    def test_eq8(self):
        text_node = TextNode("This is *text*, that *has* different `types`", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC)
        correct_split_nodes = [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.ITALIC),
                TextNode(", that ", TextType.NORMAL),
                TextNode("has", TextType.ITALIC),
                TextNode(" different `types`", TextType.NORMAL),
            ]
        self.assertEqual(split_nodes, correct_split_nodes)

    def test_eq9(self):
        text_node = TextNode("This is **text**, that *has* different `types`", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        split_nodes = split_nodes_delimiter(split_nodes, "**", TextType.BOLD)
        split_nodes = split_nodes_delimiter(split_nodes, "*", TextType.ITALIC)
        correct_split_nodes = [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(", that ", TextType.NORMAL),
                TextNode("has", TextType.ITALIC),
                TextNode(" different ", TextType.NORMAL),
                TextNode("types", TextType.CODE),
            ]
        self.assertEqual(split_nodes, correct_split_nodes)

    def test_eq10(self):
        text_node = TextNode("This is text, that has different types", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC)
        correct_split_nodes = [
                TextNode("This is text, that has different types", TextType.NORMAL),
            ]
        self.assertEqual(split_nodes, correct_split_nodes)

    def test_noteq(self):
        node = TextNode("a", TextType.BOLD, "https/dummy-site.org")
        node2 = TextNode("a", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("a", TextType.BOLD)
        node2 = TextNode("b", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq3(self):
        node = TextNode("a", TextType.BOLD)
        node2 = TextNode("a", TextType.NORMAL)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

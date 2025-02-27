import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node, extract_title
from htmlnode import LeafNode, ParentNode


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

    def test_eq11(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_matches = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected_matches)

    def test_eq12(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_matches = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected_matches)

    def test_eq13(self):
        text1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        text2 = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        nodes = [TextNode(text1, TextType.NORMAL), TextNode(text2, TextType.NORMAL)]
        expected_out = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode( "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_link(nodes), expected_out)

    def test_eq14(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        expected_out = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_nodes_link([node]), expected_out)

    def test_eq15(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) yeah", TextType.NORMAL)
        expected_out = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" yeah", TextType.NORMAL),
        ]
        self.assertEqual(split_nodes_link([node]), expected_out)

    def test_eq16(self):
        text1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        text2 = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        nodes = [TextNode(text1, TextType.NORMAL), TextNode(text2, TextType.NORMAL)]
        expected_out = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL),
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected_out)

    def test_eq17(self):
        node = TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        expected_out = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_nodes_image([node]), expected_out)

    def test_eq18(self):
        node = TextNode("This is text with a link to boot dev](https://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        expected_out = [TextNode("This is text with a link to boot dev](https://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)]
    
        self.assertEqual(split_nodes_image([node]), expected_out)

    def test_eq19(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_out = [
                            TextNode("This is ", TextType.NORMAL),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.NORMAL),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.NORMAL),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.NORMAL),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.NORMAL),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                        ]
        self.assertEqual(text_to_textnodes(text), expected_out)

    def test_eq20(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        expected_blocks = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_eq21(self):
        markdown = ""
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_eq22(self):
        markdown = "\n\n\n\n"
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_eq23(self):
        markdown = "This is a paragraph with **bold**, *italic* and `code`."
        des_out = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "This is a paragraph with "),
                LeafNode("b", "bold"),
                LeafNode(None, ", "),
                LeafNode("i", "italic"),
                LeafNode(None, " and "),
                LeafNode("code", "code"),
                LeafNode(None, "."),
            ]),
        ])
        self.assertEqual(markdown_to_html_node(markdown), des_out)

    def test_eq24(self):
        markdown = "### This is a paragraph with bold, italic and code."
        des_out = ParentNode("div", [
            ParentNode("h3", [
                LeafNode(None, "This is a paragraph with bold, italic and code."),
            ]),
        ])
        self.assertEqual(markdown_to_html_node(markdown), des_out)

    def test_eq25(self):
        markdown = "* a\n* b\n* c"
        des_out = ParentNode("div", [
            ParentNode("ul", [
                LeafNode("li", "a"),
                LeafNode("li", "b"),
                LeafNode("li", "c"),
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), des_out)

    def test_eq26(self):
        markdown = "1. a\n2. b\n3. c"
        des_out = ParentNode("div", [
            ParentNode("ol", [
                LeafNode("li", "a"),
                LeafNode("li", "b"),
                LeafNode("li", "c"),
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), des_out)

    def test_eq27(self):
        markdown = "> a\n> b\n> c"
        des_out = ParentNode("div", [
            ParentNode("blockquote", [
                LeafNode(None, "a"),
                LeafNode(None, "b"),
                LeafNode(None, "c"),
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), des_out)

    def test_eq28(self):
        markdown = "# titletitle\netihi\nteoi"
        des_out = "titletitle"
        self.assertEqual(extract_title(markdown), des_out)

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

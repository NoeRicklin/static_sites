import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "text", "**pointer**", { "key": "value" })
        node2 = HTMLNode("p", "text", "**pointer**", { "key": "value" })
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("p", "text", props={ "key": "value" })
        node2 = HTMLNode("p", "text", None, { "key": "value" })
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = HTMLNode("p", "text")
        node2 = HTMLNode("p", "text", None, {})
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = LeafNode("p", "This is a paragraph of text.")
        html_text = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), html_text)

    def test_eq5(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html_text = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), html_text)

    def test_eq6(self):
        node = LeafNode(None, "Click me!")
        html_text = "Click me!"
        self.assertEqual(node.to_html(), html_text)

    def test_eq7(self):
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html_text = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), html_text)

    def test_eq8(self):
        node = ParentNode("header",
            [
                ParentNode("bold", [
                        LeafNode("p", "Text1", { "refl": "url" }),
                        LeafNode("div", "Image", { "alt_text": "it's an image" }),
                    ], { "highlight": "Red" }
                )
            ]
        )
        html_text = '<header><bold highlight="Red"><p refl="url">Text1</p><div alt_text="it\'s an image">Image</div></bold></header>'
        self.assertEqual(node.to_html(), html_text)

    def test_noteq(self):
        node = HTMLNode("p", "", "**pointer**", { "key": "value" })
        node2 = HTMLNode("p", "text", "**pointer**", { "key": "value" })
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = HTMLNode("p", "text", "**pointer**", { "key": "value" })
        node2 = HTMLNode("p", "text", "**pointer**", { "key": "different" })
        self.assertNotEqual(node, node2)

    def test_noteq3(self):
        node = HTMLNode("p", "text", "**pointer**", { "key": "value" })
        node2 = HTMLNode("div", "text", "**pointer**", { "key": "value" })
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

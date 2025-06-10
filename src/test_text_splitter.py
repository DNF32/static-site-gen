from text_splitter import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import TextType, TextNode
import unittest


class TestTextNode(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.Text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        expect = [
            TextNode("This is text with a ", TextType.Text),
            TextNode("bolded phrase", TextType.Bold),
            TextNode(" in the middle", TextType.Text),
        ]

        for new_node in new_nodes:
            self.assertIn(new_node, expect)

    def test_split_italic(self):
        node = TextNode(
            "This is text with a __bolded phrase__ in the middle", TextType.Text
        )
        new_nodes = split_nodes_delimiter([node], "__", TextType.Italic)
        expect = [
            TextNode("This is text with a ", TextType.Text),
            TextNode("bolded phrase", TextType.Italic),
            TextNode(" in the middle", TextType.Text),
        ]

        for new_node in new_nodes:
            self.assertIn(new_node, expect)

    def test_split_bold_and_italic(self):
        node = TextNode(
            "This is text with a __bolded phrase__ **non sense** in the middle",
            TextType.Text,
        )
        new_nodes = split_nodes_delimiter([node], "__", TextType.Italic)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.Bold)
        expect = [
            TextNode("This is text with a ", TextType.Text),
            TextNode("bolded phrase", TextType.Italic),
            TextNode(" ", TextType.Text),
            TextNode("non sense", TextType.Bold),
            TextNode(" in the middle", TextType.Text),
        ]

        for new_node in new_nodes:
            self.assertIn(new_node, expect)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_no_matches(self):
        text = "This is text with a [link](https://example.com) and a broken image [obi wan](https://i.imgur.com/fJRm4Vk.jpeg"
        # Note: Missing closing parenthesis on the second "image", so it shouldn't match.

        result = extract_markdown_images(text)

        # Assert that the result is an empty list
        self.assertEqual(result, [], f"Expected no matches, but got: {result}")


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_not_matching_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        for match in extract_markdown_links(text):
            self.assertIn(match, expected)


class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.Text,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.Text),
                TextNode("image", TextType.Image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.Text),
                TextNode(
                    "second image", TextType.Image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.Text,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.Text),
                TextNode("image", TextType.Links, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.Text),
                TextNode(
                    "second image", TextType.Links, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestOrgSplitter(unittest.TestCase):
    def test_org_splitter(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.Text),
                TextNode("text", TextType.Bold),
                TextNode(" with an ", TextType.Text),
                TextNode("italic", TextType.Italic),
                TextNode(" word and a ", TextType.Text),
                TextNode("code block", TextType.Code),
                TextNode(" and an ", TextType.Text),
                TextNode(
                    "obi wan image", TextType.Image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.Text),
                TextNode("link", TextType.Links, "https://boot.dev"),
            ],
            new_nodes,
        )

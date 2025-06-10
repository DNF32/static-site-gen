import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_repr(self):
        node = HTMLNode("p", "this is a simple paragraph to make")
        printer = "HTMLNode(p,this is a simple paragraph to make,None,None)"
        self.assertEqual(node.__repr__(), printer)

    def test_diff_tag(self):
        node = HTMLNode("t", "this is a simple paragraph to make")
        printer = "HTMLNode(p,this is a simple paragraph to make,None,None)"
        self.assertNotEqual(node.__repr__(), printer)

    def test_diff_text(self):
        node = HTMLNode("this is a simple paragraph to make")
        printer = "HTMLNode(None,this is a not so simple paragraph to make,None,None)"
        self.assertNotEqual(node.__repr__(), printer)

    node1 = HTMLNode(
        tag="p", value="Hello, world!", children=None, props={"class": "text"}
    )
    node2 = HTMLNode(
        tag="strong", value="Important", children=None, props={"id": "strong1"}
    )
    node3 = HTMLNode(
        tag="div", value=None, children=[node1, node2], props={"class": "container"}
    )
    node4 = HTMLNode(tag="br", value=None, children=None, props={})
    node5 = HTMLNode(
        tag="a",
        value="Click here",
        children=None,
        props={"href": "https://example.com", "class": "container"},
    )

    def test_to_html(self):
        self.assertEqual(TestHTMLNode.node4.props_to_html(), "")
        self.assertEqual(TestHTMLNode.node3.props_to_html(), 'class="container"')
        self.assertEqual(
            TestHTMLNode.node5.props_to_html(),
            'href="https://example.com" class="container"',
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_only_leaf(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph.")
        child2 = LeafNode("p", "Second paragraph.")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>First paragraph.</p><p>Second paragraph.</p></div>",
        )

    def test_to_html_deeply_nested(self):
        deepest = LeafNode("em", "deep")
        inner = ParentNode("span", [deepest])
        middle = ParentNode("p", [inner])
        outer = ParentNode("div", [middle])
        self.assertEqual(
            outer.to_html(),
            "<div><p><span><em>deep</em></span></p></div>",
        )


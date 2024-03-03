import unittest
from lexer import Token
from parse import Parser, Node

class TestParser(unittest.TestCase):

    def test_parse_variable(self):
        parser = Parser()
        node = parser.parse_text("p")
        expected_node = Node("VARIABLE", "p")
        self.assertEqual(node, expected_node)

    def test_parse_not(self):
        parser = Parser()
        node = parser.parse_text("~p")
        expected_node = Node("NOT", "~")
        expected_node.right = Node("VARIABLE", "p")
        self.assertEqual(node, expected_node)

    def test_parse_necessarily(self):
        parser = Parser()
        node = parser.parse_text("□p")
        expected_node = Node("NECESSARILY", "□")
        expected_node.right = Node("VARIABLE", "p")
        self.assertEqual(node, expected_node)

    def test_parse_possibly(self):
        parser = Parser()
        node = parser.parse_text("◇p")
        expected_node = Node("POSSIBLY", "◇")
        expected_node.right = Node("VARIABLE", "p")
        self.assertEqual(node, expected_node)

    def test_parse_and(self):
        parser = Parser()
        node = parser.parse_text("p^q")
        expected_node = Node("AND", "^")
        expected_node.left = Node("VARIABLE", "p")
        expected_node.right = Node("VARIABLE", "q")
        self.assertEqual(node, expected_node)

    def test_parse_or(self):
        parser = Parser()
        node = parser.parse_text("p|q")
        expected_node = Node("OR", "|")
        expected_node.left = Node("VARIABLE", "p")
        expected_node.right = Node("VARIABLE", "q")
        self.assertEqual(node, expected_node)

    def test_parse_implies(self):
        parser = Parser()
        node = parser.parse_text("p->q")
        expected_node = Node("IMPLIES", "->")
        expected_node.left = Node("VARIABLE", "p")
        expected_node.right = Node("VARIABLE", "q")
        self.assertEqual(node, expected_node)

    def test_parse_complex_expression(self):
        parser = Parser()
        node = parser.parse_text("~□(p->q)^(r|s)")
        expected_node = Node("AND", "^")
        expected_node.left = Node("NOT", "~")
        expected_node.left.right = Node("NECESSARILY", "□")
        expected_node.left.right.right = Node("IMPLIES", "->")
        expected_node.left.right.right.left = Node("VARIABLE", "p")
        expected_node.left.right.right.right = Node("VARIABLE", "q")
        expected_node.right = Node("OR", "|")
        expected_node.right.left = Node("VARIABLE", "r")
        expected_node.right.right = Node("VARIABLE", "s")
        self.assertEqual(node, expected_node)

    def test_errors(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse_text(")(")    
        with self.assertRaises(SyntaxError):
            parser.parse_text("(p")     

if __name__ == '__main__':
    unittest.main()
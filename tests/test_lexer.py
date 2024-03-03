import unittest
from lexer import Lexer, Token

class TestLexer(unittest.TestCase):
    
    def test_parentheses(self):
        lexer = Lexer("()")
        tokens = lexer.tokenize()
        expected_tokens = [
            Token("LPAREN", "("),
            Token("RPAREN", ")")
        ]
        for i in range(len(tokens)):
            self.assertEqual(tokens[i].__dict__, expected_tokens[i].__dict__)
        
    def test_operators(self):
        lexer = Lexer("-> → ∧ ∨ ! ◻ ◊")
        tokens = lexer.tokenize()
        expected_tokens = [
            Token("IMPLIES", "->"),
            Token("IMPLIES", "->"),
            Token("AND", "^"),
            Token("OR", "|"),
            Token("NOT", "~"),
            Token("NECESSARILY", "□"),
            Token("POSSIBLY", "◇")
        ]
        for i in range(len(tokens)):
            self.assertEqual(tokens[i].__dict__, expected_tokens[i].__dict__)
        
    def test_variables(self):
        lexer = Lexer("p q r")
        tokens = lexer.tokenize()
        expected_tokens = [
            Token("VARIABLE", "p"),
            Token("VARIABLE", "q"),
            Token("VARIABLE", "r")
        ]
        for i in range(len(tokens)):
            self.assertEqual(tokens[i].__dict__, expected_tokens[i].__dict__)
        
    def test_errors(self):
        lexer = Lexer("&$")
        with self.assertRaises(SyntaxError):
            lexer.tokenize()
        lexer = Lexer("-")
        with self.assertRaises(SyntaxError):
            lexer.tokenize()
            
if __name__ == '__main__':
    unittest.main()
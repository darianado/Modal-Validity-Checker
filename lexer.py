import re
from typing import List

class Token:
    """
    Token class.

    Attributes
    ----------
    type: str
        Token Type.
    value: str
        Token Value.

    Methods
    -------
    __init__(self, type, value)
        Initialize the Token.
    __repr__(self)
        Return the Token.

    """
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"

class Lexer:
    """
    Lexer class.

    Attributes
    ----------
    text: str
        Text to be tokenized.
    pos: int
        Current position in the text.
    current_char: str
        Current character in the text.

    Methods
    -------
    __init__(self, text)
        Initialize the Lexer.
    error(self)
        Raise the SyntaxError.
    advance(self)
        Advance the position.
    skip_whitespace(self)
        Skip the whitespace.
    get_next_token(self)
        Return the next token.
    tokenize(self)
        Tokenize the text.

    """
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self) -> None:
        """
        Raise the SyntaxError.

        Returns
        -------
        None

        """
        raise SyntaxError("Invalid syntax")

    def advance(self) -> None:
        """
        Advance the position.

        Returns
        -------
        None

        """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self) -> None:
        """
        Skip the whitespace.

        Returns
        -------
        None

        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self) -> Token:
        """
        Return the next token.

        Returns
        -------
        Token
            Next Token.

        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '(':
                self.advance()
                return Token("LPAREN", "(")
            elif self.current_char == ')':
                self.advance()
                return Token("RPAREN", ")")
            elif self.current_char in ['~','¬','!']:
                self.advance()
                return Token("NOT", "~")
            elif self.current_char in ['^','∧','&']:
                self.advance()
                return Token("AND", "^")
            elif self.current_char in ['|','∨','v','V']:
                self.advance()
                return Token("OR", "|")
            elif self.current_char == '-':
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    return Token("IMPLIES", "->")
                else:
                    self.error()
            elif self.current_char in ['→','⇒']:
                self.advance()
                return Token("IMPLIES", "->")
            elif self.current_char in ['□','◻']:
                self.advance()
                return Token("NECESSARILY", "□")
            elif self.current_char == '[':
                self.advance()
                if self.current_char == ']':
                    self.advance()
                    return Token("NECESSARILY", "□")
                else:
                    self.error()
            elif self.current_char in ['◇','◊']:
                self.advance()
                return Token("POSSIBLY", "◇")
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    return Token("POSSIBLY", "◇")
                else:
                    self.error()
            elif re.match("[a-z]", self.current_char):
                var = ""
                while self.current_char is not None and re.match("[a-z]", self.current_char):
                    var += self.current_char
                    self.advance()
                return Token("VARIABLE", var)
            else:
                self.error()
        return Token("None", None)

    def tokenize(self) -> List[Token]:
        """
        Tokenize the text.

        Returns
        -------
        List[Token]
            List of Token.

        """
        tokens = []
        token = self.get_next_token()
        while token.type != "None":
            tokens.append(token)
            token = self.get_next_token()
        return tokens

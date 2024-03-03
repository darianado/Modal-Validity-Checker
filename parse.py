from lexer import Token, Lexer

class Node:
    """
    Encapsulate the behaviour of node.

    Attributes
    ----------
    type: str
    value: str
    left: Node
    right: Node

    Methods
    -------
    __init__(self, type, value=None)
        Initialize the node.
    __repr__(self)
        Representation of node.
    __eq__(self, other)
        Compare two nodes.
    __hash__(self)
        Hash of node.
    height(self)
        Height of node.

    """
    def __init__(self, type: str, value=None):
        self.type = type
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return f"Node({self.type}, {self.value}, {self.left}, {self.right})"

    def __eq__(self, other) -> bool:
        """
        Compare two nodes.

        Parameters
        ----------
        other: Node
            Another node to compare with.

        Returns
        -------
        bool
            True if nodes are equal, else false.

        """
        if isinstance(other, self.__class__):
            if self.value == other.value:
                if self.left == other.left:
                    if self.right == other.right:
                        return True
        return False

    def __hash__(self) -> int:
        """
        Hash of node.

        Returns
        -------
        int
            Hash of node.

        """
        return hash((self.type, self.value, self.left, self.right))

    def height(self) -> int:
        """
        Height of node.

        Returns
        -------
        int
            Height of node.

        """
        if self.left is None and self.right is None:
            return 0
        elif self.left is None:
            return 1 + self.right.height()
        elif self.right is None:
            return 1 + self.left.height()
        else:
            return 1 + max(self.left.height(), self.right.height())

class Parser:
    """
    Encapsulate the behaviour of parser.

    Attributes
    ----------
    tokens: list
        List of tokens.
    pos: int
        Current position of tokens.

    Methods
    -------
    __init__(self)
        Initialize the parser.
    error(self)
        Raise error.
    get_next_token(self)
        Get next token.
    factor(self)
        Handle the lowest-level components of the formula
    term(self)
        Handle conjunction and disjunction
    parse(self)
        Handle highest level of components, i.e implication
    parse_text(self, text: str)
        Parse the text.

    """
    def __init__(self):
        self.tokens = []
        self.pos = 0

    def error(self) -> None:
        """
        Raise error.

        Returns
        -------
        None

        """
        raise SyntaxError("Invalid syntax")

    def get_next_token(self) -> Token:
        """
        Get next token.

        Returns
        -------
        Token
            Next token.

        """
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return Token("None", None)

    def factor(self) -> Node:
        """
        Handle the lowest-level components of the formula

        Returns
        -------
        Node
            Factor.

        """
        token = self.get_next_token()
        if token.type == "VARIABLE":
            return Node("VARIABLE", token.value)
        elif token.type == "NOT":
            node = Node("NOT", token.value)
            node.right = self.factor()
            return node
        elif token.type in ["NECESSARILY", "POSSIBLY"]:
            node = Node(token.type, token.value)
            node.right = self.factor()
            return node
        elif token.type == "LPAREN":
            node = self.parse()
            if self.get_next_token().type != "RPAREN":
                self.error()
            return node
        else:
            self.error()

    def term(self) -> Node:
        """
        Handle conjunction and disjunction

        Returns
        -------
        Node
            Term.

        """
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type in ["AND", "OR"]:
            token = self.get_next_token()
            parent = Node(token.type, token.value)
            parent.left = node
            parent.right = self.factor()
            return parent
        return node

    def parse(self) -> Node:
        """
        Handle highest level of components, i.e implication

        Returns
        -------
        Node
            Parse tree.

        """
        node = self.term()
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == "IMPLIES":
            token = self.get_next_token()
            parent = Node(token.type, token.value)
            parent.left = node
            parent.right = self.term()
            return parent
        return node

    def parse_text(self, text: str) -> Node:
        """
        Parse the text.

        Parameters
        ----------
        text: str
            Text to parse.

        Returns
        -------
        Node
            Parse tree.

        """
        lexer = Lexer(text)
        self.tokens = lexer.tokenize()
        self.pos = 0
        return self.parse()


from enum import Enum, auto


class SyntaxKind(Enum):
    # Simple SyntaxToken:
    BAD_TOKEN = auto()
    END_OF_FILE_TOKEN = auto()
    WHITE_SPACE_TOKEN = auto()
    NUMBER_TOKEN = auto()
    PLUS_TOKEN = auto()
    MINUS_TOKEN = auto()
    STAR_TOKEN = auto()
    SLASH_TOKEN = auto()
    OPEN_PARENTHESIS_TOKEN = auto()
    CLOSE_PARENTHESIS_TOKEN = auto()
    IDENTIFIER_TOKEN = auto()
    BANG_TOKEN = auto()
    EQUALS_TOKEN = auto()

    # Double SyntaxToken:
    DOUBLE_EQUALS_TOKEN = auto()
    BANG_EQUALS_TOKEN = auto()
    DOUBLE_AMPERSAND_TOKEN = auto()
    DOUBLE_PIPE_TOKEN = auto()

    # ExpressionSyntax:
    LITERAL_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    PARENTHESIZED_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    NAME_EXPRESSION = auto()

    # Keyword:
    FALSE_KEYWORD = auto()
    TRUE_KEYWORD = auto()

    def get_unary_operator_precedence(self):
        if (
            self is SyntaxKind.PLUS_TOKEN or
            self is SyntaxKind.MINUS_TOKEN or
            self is SyntaxKind.BANG_TOKEN
        ):
            return 6
        else:
            return 0

    def get_binary_operator_precedence(self):
        if self is self.STAR_TOKEN or self is self.SLASH_TOKEN:
            return 5
        elif self is self.PLUS_TOKEN or self is self.MINUS_TOKEN:
            return 4
        elif self is self.DOUBLE_EQUALS_TOKEN or self is self.BANG_EQUALS_TOKEN:
            return 3
        elif self is self.DOUBLE_AMPERSAND_TOKEN:
            return 2
        elif self is self.DOUBLE_PIPE_TOKEN:
            return 1
        else:
            return 0

    @classmethod
    def get_keyword_kind(cls, string):
        if string == "true":
            return cls.TRUE_KEYWORD
        elif string == "false":
            return cls.FALSE_KEYWORD
        else:
            return cls.IDENTIFIER_TOKEN

from enum import Enum


class SyntaxKind(Enum):

    BAD_TOKEN = 1,
    END_OF_FILE_TOKEN = 2,
    WHITE_SPACE_TOKEN = 3,
    NUMBER_TOKEN = 4,
    PLUS_TOKEN = 5,
    MINUS_TOKEN = 6,
    STAR_TOKEN = 7,
    SLASH_TOKEN = 8,
    OPEN_PARENTHESIS_TOKEN = 9,
    CLOSE_PARENTHESIS_TOKEN = 10,

    LITERAL_EXPRESSION = 11,
    BINARY_EXPRESSION = 12,
    UNARY_EXPRESSION = 13,
    PARENTHESIZED_EXPRESSION = 14

    def get_unary_operator_precedence(self):
        if (self is SyntaxKind.PLUS_TOKEN or
                self is SyntaxKind.MINUS_TOKEN):
            return 3
        else:
            return 0

    def get_binary_operator_precedence(self):
        if (self is SyntaxKind.STAR_TOKEN or
                self is SyntaxKind.SLASH_TOKEN):
            return 2
        elif (self is SyntaxKind.PLUS_TOKEN or
              self is SyntaxKind.MINUS_TOKEN):
            return 1
        else:
            return 0

from enum import Enum


class SyntaxKind(Enum):
    BadToken = 1,
    EndOfFileToken = 2,
    WhiteSpaceToken = 3,
    NumberToken = 4,
    PlusToken = 5,
    MinusToken = 6,
    StarToken = 7,
    SlashToken = 8,
    OpenParenthesisToken = 9,
    CloseParenthesisToken = 10,

    LiteralExpression = 11,
    BinaryExpression = 12,
    UnaryExpression = 13,
    ParenthesizedExpression = 14

    def get_unary_operator_precedence(self):
        if (self is SyntaxKind.PlusToken or
                self is SyntaxKind.MinusToken):
            return 3
        else:
            return 0

    def get_binary_operator_precedence(self):
        if (self is SyntaxKind.StarToken or
                self is SyntaxKind.SlashToken):
            return 2
        elif (self is SyntaxKind.PlusToken or
                self is SyntaxKind.MinusToken):
            return 1
        else:
            return 0
from abc import ABC, abstractmethod
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

    NumberExpression = 11,
    BinaryExpression = 12,
    ParenthesizedExpression = 13


class SyntaxNode(ABC):

    def __init__(self, syntaxkind):
        self.syntaxkind = syntaxkind

    @abstractmethod
    def get_children(self):
        raise StopIteration


class SyntaxToken(SyntaxNode):

    def __init__(self, syntaxkind, position, string, value):
        super().__init__(syntaxkind)
        self.position = position
        self.string = string
        self.value = value

    def get_children(self):
        raise StopIteration


class ExpressionSyntax(SyntaxNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_children(self):
        raise StopIteration


class LiteralExpressionSyntax(ExpressionSyntax):

    def __init__(self, literaltoken):
        super().__init__(SyntaxKind.NumberExpression)
        self.literaltoken = literaltoken

    def get_children(self):
        yield self.literaltoken


class BinaryExpressionSyntax(ExpressionSyntax):

    def __init__(self, left, operatortoken, right):
        super().__init__(SyntaxKind.BinaryExpression)
        self.left = left
        self.right = right
        self.operatortoken = operatortoken

    def get_children(self):
        yield self.left
        yield self.operatortoken
        yield self.right


class ParenthesizedExpressionSyntax(ExpressionSyntax):

    def __init__(self, open_parenthesis_token, expression, close_parenthesis_token):
        super().__init__(SyntaxKind.ParenthesizedExpression)
        self.open_parenthesis_token = open_parenthesis_token
        self.expression = expression
        self.close_parenthesis_token = close_parenthesis_token

    def get_children(self):
        yield self.open_parenthesis_token
        yield self.expression
        yield self.close_parenthesis_token

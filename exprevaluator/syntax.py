from abc import ABC, abstractmethod
from enum import Enum


class SyntaxKind(Enum):

    NumberToken = 0,
    SpaceToken = 1,
    PlusToken = 2,
    MinusToken = 3,
    StarToken = 4,
    SlashToken = 5,
    OpenParenthesisToken = 6,
    CloseParenthesisToken = 7,
    BadToken = 8,
    EndOfFileToken = 9,
    NumberExpression = 10,
    BinaryExpression = 11,
    ParenthesizedExpression = 12


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


class NumberExpressionSyntax(ExpressionSyntax):

    def __init__(self, numbertoken):
        super().__init__(SyntaxKind.NumberExpression)
        self.numbertoken = numbertoken

    def get_children(self):
        yield self.numbertoken


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

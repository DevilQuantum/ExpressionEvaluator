from .expression_syntax import ExpressionSyntax
from .syntax_kind import SyntaxKind


class BinaryExpressionSyntax(ExpressionSyntax):

    def __init__(self, left, operator_token, right):
        super().__init__(SyntaxKind.BINARY_EXPRESSION)
        self.left = left
        self.right = right
        self.operator_token = operator_token

    def get_children(self):
        yield self.left
        yield self.operator_token
        yield self.right

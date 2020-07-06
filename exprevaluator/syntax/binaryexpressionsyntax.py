from .expressionsyntax import ExpressionSyntax
from .syntaxkind import SyntaxKind


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
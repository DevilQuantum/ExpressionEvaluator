from .expressionsyntax import ExpressionSyntax
from .syntaxkind import SyntaxKind


class UnaryExpressionSyntax(ExpressionSyntax):

    def __init__(self, operatortoken, operand):
        super().__init__(SyntaxKind.UnaryExpression)
        self.operatortoken = operatortoken
        self.operand = operand

    def get_children(self):
        yield self.operatortoken
        yield self.operand
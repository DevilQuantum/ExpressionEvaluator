from .expression_syntax import ExpressionSyntax
from .syntax_kind import SyntaxKind


class UnaryExpressionSyntax(ExpressionSyntax):

    def __init__(self, operator_token, operand):
        super().__init__(SyntaxKind.UNARY_EXPRESSION)
        self.operator_token = operator_token
        self.operand = operand

    def get_children(self):
        yield self.operator_token
        yield self.operand

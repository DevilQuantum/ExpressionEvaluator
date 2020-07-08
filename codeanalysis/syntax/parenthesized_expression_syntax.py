from .expression_syntax import ExpressionSyntax
from .syntax_kind import SyntaxKind


class ParenthesizedExpressionSyntax(ExpressionSyntax):

    def __init__(self, open_parenthesis_token, expression, close_parenthesis_token):
        super().__init__(SyntaxKind.PARENTHESIZED_EXPRESSION)
        self.open_parenthesis_token = open_parenthesis_token
        self.expression = expression
        self.close_parenthesis_token = close_parenthesis_token

    def get_children(self):
        yield self.open_parenthesis_token
        yield self.expression
        yield self.close_parenthesis_token

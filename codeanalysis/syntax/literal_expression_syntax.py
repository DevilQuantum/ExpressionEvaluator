from .expression_syntax import ExpressionSyntax
from .syntax_kind import SyntaxKind


class LiteralExpressionSyntax(ExpressionSyntax):

    def __init__(self, literal_token, value=None):
        super().__init__(SyntaxKind.LITERAL_EXPRESSION)
        self.literal_token = literal_token
        self.value = literal_token.value if value is None else value

    def get_children(self):
        yield self.literal_token

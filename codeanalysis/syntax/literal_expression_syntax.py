from .expression_syntax import ExpressionSyntax
from .syntax_kind import SyntaxKind


class LiteralExpressionSyntax(ExpressionSyntax):

    def __init__(self, literaltoken):
        super().__init__(SyntaxKind.LITERAL_EXPRESSION)
        self.literaltoken = literaltoken

    def get_children(self):
        yield self.literaltoken

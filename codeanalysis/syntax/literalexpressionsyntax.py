from .expressionsyntax import ExpressionSyntax
from .syntaxkind import SyntaxKind


class LiteralExpressionSyntax(ExpressionSyntax):

    def __init__(self, literaltoken):
        super().__init__(SyntaxKind.LiteralExpression)
        self.literaltoken = literaltoken

    def get_children(self):
        yield self.literaltoken

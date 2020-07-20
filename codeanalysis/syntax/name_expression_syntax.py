from codeanalysis.syntax.expression_syntax import ExpressionSyntax
from codeanalysis.syntax.syntax_kind import SyntaxKind


class NameExpressionSyntax(ExpressionSyntax):

    def __init__(self, identifier_token):
        super().__init__(SyntaxKind.NAME_EXPRESSION)
        self.identifier_token = identifier_token

    def get_children(self):
        yield self.identifier_token

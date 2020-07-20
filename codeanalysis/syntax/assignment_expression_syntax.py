from codeanalysis.syntax.expression_syntax import ExpressionSyntax
from codeanalysis.syntax.syntax_kind import SyntaxKind


class AssignmentExpressionSyntax(ExpressionSyntax):

    def __init__(self, identifier_token, equals_token, expression):
        super().__init__(SyntaxKind.ASSIGNMENT_EXPRESSION)
        self.identifier_token = identifier_token
        self.equals_token = equals_token
        self.expression = expression

    def get_children(self):
        yield self.identifier_token
        yield self.equals_token
        yield self.expression

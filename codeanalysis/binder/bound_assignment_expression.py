from codeanalysis.binder.bound_expression import BoundExpression
from codeanalysis.binder.bound_node_kind import BoundNodeKind


class BoundAssignmentExpression(BoundExpression):

    def __init__(self, variable, expression):
        super().__init__(BoundNodeKind.ASSIGNMENT_EXPRESSION)
        self.variable = variable
        self.expression = expression
        self.type = expression.type

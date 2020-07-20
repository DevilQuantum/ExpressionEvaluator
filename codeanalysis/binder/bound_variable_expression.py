from codeanalysis.binder.bound_expression import BoundExpression
from codeanalysis.binder.bound_node_kind import BoundNodeKind


class BoundVariableExpression(BoundExpression):

    def __init__(self, variable):
        super().__init__(BoundNodeKind.VARIABLE_EXPRESSION)
        self.variable = variable
        self.type = variable.type

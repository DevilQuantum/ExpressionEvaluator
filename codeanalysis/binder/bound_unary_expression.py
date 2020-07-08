from codeanalysis.binder.bound_expression import BoundExpression
from codeanalysis.binder.bound_node_kind import BoundNodeKind


class BoundUnaryExpression(BoundExpression):

    def __init__(self, operator_kind, operand):
        super().__init__(BoundNodeKind.UNARY_EXPRESSION)
        self.operator_kind = operator_kind
        self.operand = operand

    @property
    def type(self):
        return self.operand.type
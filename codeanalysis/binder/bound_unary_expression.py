from .bound_expression import BoundExpression
from .bound_node_kind import BoundNodeKind


class BoundUnaryExpression(BoundExpression):

    def __init__(self, operator, operand):
        super().__init__(BoundNodeKind.UNARY_EXPRESSION)
        self.operator = operator
        self.operand = operand
        self.type = operator.result_type

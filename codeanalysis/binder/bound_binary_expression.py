from codeanalysis.binder.bound_expression import BoundExpression
from codeanalysis.binder.bound_node_kind import BoundNodeKind


class BoundBinaryExpression(BoundExpression):

    def __init__(self, left, operator_kind, right):
        super().__init__(BoundNodeKind.UNARY_EXPRESSION)
        self.left = left
        self.operator_kind = operator_kind
        self.right = right

    @property
    def type(self):
        return self.left.type
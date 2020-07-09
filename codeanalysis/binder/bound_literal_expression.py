from .bound_expression import BoundExpression
from .bound_node_kind import BoundNodeKind


class BoundLiteralExpression(BoundExpression):

    def __init__(self, value):
        super().__init__(BoundNodeKind.LITERAL_EXPRESSION)
        self.value = value

    @property
    def type(self):
        return type(self.value)

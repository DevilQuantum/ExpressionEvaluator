from .binder.bound_binary_expression import BoundBinaryExpression
from .binder.bound_unary_expression import BoundUnaryExpression
from .binder.bound_literal_expression import BoundLiteralExpression
from .binder.bound_binary_operator_kind import BoundBinaryOperatorKind
from .binder.bound_unary_operator_kind import BoundUnaryOperatorKind


class Evaluator:

    def __init__(self, bound_expression):
        self._root = bound_expression

    def evaluate(self):
        return self.evaluate_expression(self._root)

    def evaluate_expression(self, node):
        if isinstance(node, BoundLiteralExpression):
            return int(node.value)

        elif isinstance(node, BoundBinaryExpression):
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)

            if node.operator_kind is BoundBinaryOperatorKind.ADDITION:
                return left + right
            elif node.operator_kind is BoundBinaryOperatorKind.SUBTRACTION:
                return left - right
            elif node.operator_kind is BoundBinaryOperatorKind.MULTIPLICATION:
                return left * right
            elif node.operator_kind is BoundBinaryOperatorKind.DIVISION:
                return left // right
            else:
                print(node.operator_kind)
                print(type(node))
                raise Exception(f"""Unexpected binary operator '{node.operator_kind}'""")

        elif isinstance(node, BoundUnaryExpression):
            operand = int(self.evaluate_expression(node.operand))
            if node.operator_kind is BoundUnaryOperatorKind.Identity:
                return operand
            if node.operator_kind is BoundUnaryOperatorKind.Negation:
                return -operand
            else:
                raise Exception(f"""Unexpected unary operator '{node.operator_kind}'""")

        else:
            raise Exception(f"""Unexpected node '{node.operator_kind}'""")

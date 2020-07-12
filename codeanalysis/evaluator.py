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
        if type(node) is BoundLiteralExpression:
            return node.value
        elif type(node) is BoundBinaryExpression:
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)
            if node.operator.kind is BoundBinaryOperatorKind.ADDITION:
                return int(left) + int(right)
            elif node.operator.kind is BoundBinaryOperatorKind.SUBTRACTION:
                return int(left) - int(right)
            elif node.operator.kind is BoundBinaryOperatorKind.MULTIPLICATION:
                return int(left) * int(right)
            elif node.operator.kind is BoundBinaryOperatorKind.DIVISION:
                return int(left) // int(right)
            elif node.operator.kind is BoundBinaryOperatorKind.LOGICAL_AND:
                return bool(left) and bool(right)
            elif node.operator.kind is BoundBinaryOperatorKind.LOGICAL_OR:
                return bool(left) or bool(right)
            else:
                raise Exception(f"""Unexpected binary operator '{node.operator}'""")
        elif type(node) is BoundUnaryExpression:
            operand = self.evaluate_expression(node.operand)
            if node.operator.kind is BoundUnaryOperatorKind.IDENTITY:
                return int(operand)
            elif node.operator.kind is BoundUnaryOperatorKind.NEGATION:
                return int(-operand)
            elif node.operator.kind is BoundUnaryOperatorKind.LOGICAL_NEGATION:
                return not bool(operand)
            else:
                raise Exception(f"""Unexpected unary operator '{node.operator}'""")
        else:
            raise Exception(f"""Unexpected node '{node.kind}'""")

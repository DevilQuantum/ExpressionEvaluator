import logging

from .bound_binary_expression import BoundBinaryExpression
from .bound_binary_operator_kind import BoundBinaryOperatorKind
from .bound_literal_expression import BoundLiteralExpression
from .bound_unary_expression import BoundUnaryExpression
from .bound_unary_operator_kind import BoundUnaryOperatorKind
from ..syntax.syntax_kind import SyntaxKind


class Binder:

    def __init__(self):
        self.diagnostics = []

    def bind_expression(self, syntax):
        if syntax.kind is SyntaxKind.LITERAL_EXPRESSION:
            return self._bind_literal_expression(syntax)
        elif syntax.kind is SyntaxKind.UNARY_EXPRESSION:
            return self._bind_unary_expression(syntax)
        elif syntax.kind is SyntaxKind.BINARY_EXPRESSION:
            return self._bind_binary_expression(syntax)
        elif syntax.kind is SyntaxKind.PARENTHESIZED_EXPRESSION:
            return self.bind_expression(syntax.expression)
        else:
            raise Exception(f'Unexpected syntax {syntax.kind}')

    def _bind_literal_expression(self, syntax):
        value = int(syntax.literaltoken.value or 0)
        return BoundLiteralExpression(value)

    def _bind_unary_expression(self, syntax):
        bound_operand = self.bind_expression(syntax.operand)
        bound_operator_kind = self._bind_unary_operator_kind(syntax.operator_token.kind, bound_operand.type)

        if bound_operator_kind is None:
            self.diagnostics.append((
                f"""Unary operator '{syntax.operator_token.text}' is not defined for type '{type(bound_operand)}'""",
                logging.ERROR)
            )
        return BoundUnaryExpression(bound_operator_kind, bound_operand)

    def _bind_binary_expression(self, syntax):
        bound_left = self.bind_expression(syntax.left)
        bound_right = self.bind_expression(syntax.right)
        bound_operator_kind = self._bind_binary_operator_kind(
            syntax.operator_token.kind,
            bound_left.type,
            bound_right.type
        )

        if bound_operator_kind is None:
            self.diagnostics.append((
                f"""Binary operator '{syntax.operator_token.text}' is not defined for types 
                '{type(bound_left.value)}' and '{type(bound_right.value)}'""",
                logging.ERROR)
            )
        return BoundBinaryExpression(bound_left, bound_operator_kind, bound_right)

    def _bind_unary_operator_kind(self, kind, operand_type):
        if operand_type is not int:
            return None

        if kind is SyntaxKind.PLUS_TOKEN:
            return BoundUnaryOperatorKind.Identity
        elif kind is SyntaxKind.MINUS_TOKEN:
            return BoundUnaryOperatorKind.Negation
        else:
            raise Exception(f'Unexpected unary operator {kind}')

    def _bind_binary_operator_kind(self, kind, left_type, right_type):
        if left_type is not int or right_type is not int:
            return None

        if kind is SyntaxKind.PLUS_TOKEN:
            return BoundBinaryOperatorKind.ADDITION
        elif kind is SyntaxKind.MINUS_TOKEN:
            return BoundBinaryOperatorKind.SUBTRACTION
        elif kind is SyntaxKind.STAR_TOKEN:
            return BoundBinaryOperatorKind.MULTIPLICATION
        elif kind is SyntaxKind.SLASH_TOKEN:
            return BoundBinaryOperatorKind.DIVISION
        else:
            raise Exception(f'Unexpected binary operator {kind}')

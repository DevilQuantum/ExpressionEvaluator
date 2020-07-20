import logging

from .bound_assignment_expression import BoundAssignmentExpression
from .bound_binary_expression import BoundBinaryExpression
from .bound_binary_operator import BoundBinaryOperator
from .bound_literal_expression import BoundLiteralExpression
from .bound_unary_expression import BoundUnaryExpression
from .bound_unary_operator import BoundUnaryOperator
from .bound_variable_expression import BoundVariableExpression
from ..diagnostic import DiagnosticBag
from ..syntax.syntax_kind import SyntaxKind
from ..variable_symbol import VariableSymbol


class Binder:

    def __init__(self, variables):
        self.diagnostic_bag = DiagnosticBag()
        self._variables = variables

    def bind_expression(self, syntax):
        if syntax.kind is SyntaxKind.PARENTHESIZED_EXPRESSION:
            return self._bind_parenthesized_expression(syntax)
        elif syntax.kind is SyntaxKind.LITERAL_EXPRESSION:
            return self._bind_literal_expression(syntax)
        elif syntax.kind is SyntaxKind.NAME_EXPRESSION:
            return self._bind_name_expression(syntax)
        elif syntax.kind is SyntaxKind.ASSIGNMENT_EXPRESSION:
            return self._bind_assignment_expression(syntax)
        elif syntax.kind is SyntaxKind.UNARY_EXPRESSION:
            return self._bind_unary_expression(syntax)
        elif syntax.kind is SyntaxKind.BINARY_EXPRESSION:
            return self._bind_binary_expression(syntax)
        else:
            raise Exception(f'Unexpected syntax {syntax.kind}')

    def _bind_parenthesized_expression(self, syntax):
        return self.bind_expression(syntax.expression)

    def _bind_literal_expression(self, syntax):
        value = 0 if syntax.value is None else syntax.value
        return BoundLiteralExpression(value)

    def _bind_name_expression(self, syntax):
        name = syntax.identifier_token.text
        variable = next((v for v in self._variables if v.name == name), None)
        if variable is None:
            self.diagnostic_bag.report_undefined_name(syntax.identifier_token.text_span, name, logging.ERROR)
            return BoundLiteralExpression(0)
        else:
            return BoundVariableExpression(variable)

    def _bind_assignment_expression(self, syntax):
        name = syntax.identifier_token.text
        bound_expression = self.bind_expression(syntax.expression)
        # default_value = (
        #     None if bound_expression is None else 0 if bound_expression.type is int else False if bound_expression.type is bool else None # noqa
        # )
        existing_variable = next((v for v in self._variables if v.name == name), None)
        if existing_variable is not None:
            del self._variables[name]
        variable = VariableSymbol(name, bound_expression.type)
        self._variables[variable] = None
        return BoundAssignmentExpression(variable, bound_expression)
        # if default_value is None:
        #    raise Exception(f'Unsupported variable type: {bound_expression.type}')

    def _bind_unary_expression(self, syntax):
        bound_operand = self.bind_expression(syntax.operand)
        bound_operator = BoundUnaryOperator.bind(syntax.operator_token.kind, bound_operand.type)
        if bound_operator is None:
            self.diagnostic_bag.report_undefined_unary_operator(
                syntax.operator_token.text_span,
                syntax.operator_token.text,
                bound_operand.type,
                logging.ERROR
            )
            return bound_operand
        else:
            return BoundUnaryExpression(bound_operator, bound_operand)

    def _bind_binary_expression(self, syntax):
        bound_left = self.bind_expression(syntax.left)
        bound_right = self.bind_expression(syntax.right)
        bound_operator = BoundBinaryOperator.bind(
            syntax.operator_token.kind,
            bound_left.type,
            bound_right.type
        )
        if bound_operator is None:
            self.diagnostic_bag.report_undefined_binary_operator(
                syntax.operator_token.text_span,
                syntax.operator_token.text,
                bound_left.type,
                bound_right.type,
                logging.ERROR
            )
            return bound_left
        else:
            return BoundBinaryExpression(bound_left, bound_operator, bound_right)

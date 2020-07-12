from .bound_unary_operator_kind import BoundUnaryOperatorKind
from ..syntax.syntax_kind import SyntaxKind


class BoundUnaryOperator:

    def __init__(self, syntax_kind, kind, operand_type, result_type=None):
        self.syntax_kind = syntax_kind
        self.kind = kind
        self.operand_type = operand_type
        self.result_type = operand_type if result_type is None else result_type

    @staticmethod
    def bind(syntax_kind, operand_type):
        for op in operators:
            if op.syntax_kind is syntax_kind and op.operand_type is operand_type:
                return op


operators = [
    BoundUnaryOperator(SyntaxKind.BANG_TOKEN, BoundUnaryOperatorKind.LOGICAL_NEGATION, bool),
    BoundUnaryOperator(SyntaxKind.PLUS_TOKEN, BoundUnaryOperatorKind.IDENTITY, int),
    BoundUnaryOperator(SyntaxKind.MINUS_TOKEN, BoundUnaryOperatorKind.NEGATION, int)
]

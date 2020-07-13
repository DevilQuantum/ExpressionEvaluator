from .bound_binary_operator_kind import BoundBinaryOperatorKind
from ..syntax.syntax_kind import SyntaxKind


class BoundBinaryOperator:

    def __init__(
            self, syntax_kind, kind, left_type, right_type=None, result_type=None
    ):
        self.syntax_kind = syntax_kind
        self.kind = kind
        self.left_type = left_type
        self.right_type = left_type if right_type is None else right_type
        self.result_type = left_type if result_type is None else result_type

    @staticmethod
    def bind(syntax_kind, left_type, right_type):
        for op in operators:
            if (
                op.syntax_kind is syntax_kind and
                op.left_type is left_type and
                op.right_type is right_type
            ):
                return op


operators = [
    BoundBinaryOperator(
        SyntaxKind.PLUS_TOKEN,
        BoundBinaryOperatorKind.ADDITION,
        int
    ),
    BoundBinaryOperator(
        SyntaxKind.MINUS_TOKEN,
        BoundBinaryOperatorKind.SUBTRACTION,
        int
    ),


    BoundBinaryOperator(
        SyntaxKind.STAR_TOKEN,
        BoundBinaryOperatorKind.MULTIPLICATION,
        int
    ),
    BoundBinaryOperator(
        SyntaxKind.SLASH_TOKEN,
        BoundBinaryOperatorKind.DIVISION,
        int
    ),


    BoundBinaryOperator(
        SyntaxKind.DOUBLE_EQUALS_TOKEN,
        BoundBinaryOperatorKind.EQUALS,
        int,
        None,
        bool
    ),
    BoundBinaryOperator(
        SyntaxKind.BANG_EQUALS_TOKEN,
        BoundBinaryOperatorKind.NOT_EQUALS,
        int,
        None,
        bool
    ),


    BoundBinaryOperator(
        SyntaxKind.DOUBLE_AMPERSAND_TOKEN,
        BoundBinaryOperatorKind.LOGICAL_AND,
        bool
    ),
    BoundBinaryOperator(
        SyntaxKind.DOUBLE_PIPE_TOKEN,
        BoundBinaryOperatorKind.LOGICAL_OR,
        bool
    ),


    BoundBinaryOperator(
        SyntaxKind.DOUBLE_EQUALS_TOKEN,
        BoundBinaryOperatorKind.EQUALS,
        bool
    ),
    BoundBinaryOperator(
        SyntaxKind.BANG_EQUALS_TOKEN,
        BoundBinaryOperatorKind.NOT_EQUALS,
        bool
    )
]

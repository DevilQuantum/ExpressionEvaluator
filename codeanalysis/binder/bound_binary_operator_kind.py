from enum import Enum


class BoundBinaryOperatorKind(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    LOGICAL_AND = 5
    LOGICAL_OR = 6
    EQUALS = 7
    NOT_EQUALS = 8

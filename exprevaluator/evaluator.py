from .syntax.binaryexpressionsyntax import BinaryExpressionSyntax
from .syntax.literalexpressionsyntax import LiteralExpressionSyntax
from .syntax.parenthesizedexpressionsyntax import ParenthesizedExpressionSyntax
from .syntax.syntaxkind import SyntaxKind
from .syntax.unaryexpressionsyntax import UnaryExpressionSyntax


class Evaluator:

    def __init__(self, expressionsyntax):
        self.root = expressionsyntax

    def evaluate(self):
        return self.evaluate_expression(self.root)

    def evaluate_expression(self, node):
        if isinstance(node, LiteralExpressionSyntax):
            return int(node.literaltoken.value)

        elif isinstance(node, BinaryExpressionSyntax):
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)

            if node.operatortoken.syntaxkind is SyntaxKind.PlusToken:
                return left + right
            elif node.operatortoken.syntaxkind is SyntaxKind.MinusToken:
                return left - right
            elif node.operatortoken.syntaxkind is SyntaxKind.StarToken:
                return left * right
            elif node.operatortoken.syntaxkind is SyntaxKind.SlashToken:
                return left // right
            else:
                raise Exception(f"""Unexpected binary operator '{node.operatortoken.syntaxkind}'""")

        elif isinstance(node, UnaryExpressionSyntax):
            operand = self.evaluate_expression(node.operand)
            if node.operatortoken.syntaxkind is SyntaxKind.PlusToken:
                return operand
            if node.operatortoken.syntaxkind is SyntaxKind.MinusToken:
                return -operand
            else:
                raise Exception(f"""Unexpected unary operator '{node.operatortoken.syntaxkind}'""")

        elif isinstance(node, ParenthesizedExpressionSyntax):
            return self.evaluate_expression(node.expression)

        else:
            raise Exception(f"""Unexpected node '{node.syntaxkind}'""")

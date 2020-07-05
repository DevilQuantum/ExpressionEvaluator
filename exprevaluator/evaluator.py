from .syntax import SyntaxKind, LiteralExpressionSyntax, BinaryExpressionSyntax, \
    ParenthesizedExpressionSyntax


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

            if node.operatortoken.syntaxkind == SyntaxKind.PlusToken:
                return left + right
            elif node.operatortoken.syntaxkind == SyntaxKind.MinusToken:
                return left - right
            elif node.operatortoken.syntaxkind == SyntaxKind.StarToken:
                return left * right
            elif node.operatortoken.syntaxkind == SyntaxKind.SlashToken:
                return left // right
            else:
                raise Exception(f"""Unexpected operator '{node.operatortoken.syntaxkind}'""")

        elif isinstance(node, ParenthesizedExpressionSyntax):
            return self.evaluate_expression(node.expression)

        else:
            raise Exception(f"""Unexpected node '{node.syntaxkind}'""")

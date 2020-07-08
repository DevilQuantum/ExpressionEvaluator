from .syntax_node import SyntaxNode


class ExpressionSyntax(SyntaxNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_children(self):
        raise StopIteration

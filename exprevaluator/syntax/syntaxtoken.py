from .syntaxnode import SyntaxNode


class SyntaxToken(SyntaxNode):

    def __init__(self, syntaxkind, position, string, value):
        super().__init__(syntaxkind)
        self.position = position
        self.string = string
        self.value = value

    def get_children(self):
        raise StopIteration
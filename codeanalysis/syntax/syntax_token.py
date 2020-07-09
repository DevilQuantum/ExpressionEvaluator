from .syntax_node import SyntaxNode


class SyntaxToken(SyntaxNode):

    def __init__(self, kind, position, text, value):
        super().__init__(kind)
        self.position = position
        self.text = text
        self.value = value

    def get_children(self):
        raise StopIteration

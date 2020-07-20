from .syntax_node import SyntaxNode
from ..text_span import TextSpan


class SyntaxToken(SyntaxNode):

    def __init__(self, kind, position, text, value):
        super().__init__(kind)
        self.position = position
        self.text = text
        self.value = value
        self.text_span = TextSpan(self.position, len(self.text))

from .syntax_node import SyntaxNode
from ..text_span import TextSpan


class SyntaxToken(SyntaxNode):

    def __init__(self, kind, position, text, value):
        super().__init__(kind)
        self.position = position
        self.text = text
        self.value = value

    @property
    def text_span(self):
        return TextSpan(self.position, len(self.text))

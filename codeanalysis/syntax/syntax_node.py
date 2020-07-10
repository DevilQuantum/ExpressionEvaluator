from abc import ABC


class SyntaxNode(ABC):

    def __init__(self, syntax_kind):
        self.kind = syntax_kind

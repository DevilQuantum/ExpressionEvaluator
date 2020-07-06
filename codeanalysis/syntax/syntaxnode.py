from abc import ABC, abstractmethod


class SyntaxNode(ABC):

    def __init__(self, syntaxkind):
        self.syntaxkind = syntaxkind

    @abstractmethod
    def get_children(self):
        raise StopIteration
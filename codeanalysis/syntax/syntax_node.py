from abc import ABC, abstractmethod


class SyntaxNode(ABC):

    def __init__(self, syntax_kind):
        self.kind = syntax_kind

    @abstractmethod
    def get_children(self):
        raise StopIteration

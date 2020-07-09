from abc import ABC


class BoundNode(ABC):

    def __init__(self, bound_node_kind):
        self.kind = bound_node_kind

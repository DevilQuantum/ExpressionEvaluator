from .bound_node import BoundNode


class BoundExpression(BoundNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

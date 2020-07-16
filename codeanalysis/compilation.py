from .evaluation_result import EvaluationResult
from .binder.binder import Binder
from .evaluator import Evaluator


class Compilation:

    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree

    def evaluate(self):
        binder = Binder()
        bound_expression = binder.bind_expression(self.syntax_tree.root)

        diagnostic_bag = self.syntax_tree.diagnostic_bag
        diagnostic_bag.diagnostics.extend(
            binder.diagnostic_bag.diagnostics
        )
        if diagnostic_bag.diagnostics:
            return EvaluationResult(diagnostic_bag, None)
        else:
            evaluator = Evaluator(bound_expression)
            value = evaluator.evaluate()
            return EvaluationResult(diagnostic_bag, value)

import logging
import os
import subprocess

from .evaluator import Evaluator
from .parser import SyntaxTree
from .syntax import SyntaxToken


def main():

    def pretty_print(node, indent='', is_last=True):
        marker = '└──' if is_last else '├──'
        print(indent, end='')
        print(marker, end='')
        print(node.syntaxkind, end='')

        if isinstance(node, SyntaxToken) and node.value is not None:
            print(':   ' + str(node.value), end='')

        print()
        *_, last_child = node.get_children()

        indent += '    ' if is_last else '│   '
        for child in node.get_children():
            try:
                pretty_print(child, indent, child == last_child)
            except StopIteration:
                continue

    def clear():
        if os.name in ('nt', 'dos'):
            subprocess.call('cls', shell=True)
        elif os.name in ('linux', 'osx', 'posix'):
            subprocess.call("clear")
        else:
            for _ in range(120):
                print('\n')

    def process_input():
        nonlocal show_tree
        if term == '' or term.isspace() or term is None:
            print('You have to enter a valid term\n')
            return
        elif term == '#showtree':
            show_tree = not show_tree
            print('Showing parse trees' if show_tree else 'Hiding parse trees')
            return
        elif term == '#cls' or term == '#clear':
            clear()
            return

        syntaxtree = SyntaxTree.parse(term, logger)
        if show_tree:
            pretty_print(syntaxtree.root)

        if syntaxtree.has_diagnostics():
            syntaxtree.report_diagnostics()
        else:
            evaluator = Evaluator(syntaxtree.root)
            result = evaluator.evaluate()
            print(result)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    show_tree = False
    while True:
        term = input('Enter a mathematical term\n')
        process_input()


if __name__ == "__main__":
    main()

import logging
import os
import subprocess
import colorama

from .compilation import Compilation
from .syntax.parser import SyntaxTree
from .syntax.syntax_token import SyntaxToken


def main():

    def pretty_print(node, indent='', is_last=True):
        marker = '└──' if is_last else '├──'
        print(indent, end='')
        print(marker, end='')
        print(node.kind.name, end='')
        if isinstance(node, SyntaxToken):
            if node.value is not None:
                print(':   ' + str(node.value), end='')
            print()
        else:
            print()
            indent += '    ' if is_last else '│   '
            *_, last_child = node.get_children()
            for child in node.get_children():
                pretty_print(child, indent, child == last_child)

    def clear():
        if os.name in ('nt', 'dos'):
            subprocess.call('cls', shell=True)
        elif os.name in ('linux', 'osx', 'posix'):
            subprocess.call("clear")
        else:
            for _ in range(120):

                print('\n')

    def process_input():
        print()
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

        syntax_tree = SyntaxTree.parse(term)
        compilation = Compilation(syntax_tree)
        result = compilation.evaluate(variables)
        diagnostic_bag = result.diagnostic_bag
        if show_tree:
            pretty_print(syntax_tree.root)

        if diagnostic_bag.diagnostics:
            for diagnostic in diagnostic_bag.diagnostics:
                print(colorama.Fore.RED)
                prefix = term[:diagnostic.text_span.start]
                error = term[diagnostic.text_span.start:diagnostic.text_span.end]
                suffix = term[diagnostic.text_span.end:]
                logger.log(
                    diagnostic.level,
                    f'{colorama.Fore.RED}{diagnostic}'
                    f'\nTEXT:            '
                    f'{colorama.Fore.GREEN}{prefix}'
                    f'{colorama.Fore.RED}{error}'
                    f'{colorama.Fore.GREEN}{suffix}{colorama.Style.RESET_ALL}'
                )
                print()
        else:
            print(result.value)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    show_tree = False
    variables = {}
    while True:
        term = input('Enter a mathematical term\n')
        process_input()


if __name__ == "__main__":
    colorama.init()
    main()

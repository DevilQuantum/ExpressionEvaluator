import logging

from .assignment_expression_syntax import AssignmentExpressionSyntax
from .binary_expression_syntax import BinaryExpressionSyntax
from .lexer import Lexer
from .name_expression_syntax import NameExpressionSyntax
from .syntax_kind import SyntaxKind
from .literal_expression_syntax import LiteralExpressionSyntax
from .parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from .syntax_token import SyntaxToken
from .unary_expression_syntax import UnaryExpressionSyntax
from ..diagnostic import DiagnosticBag


class Parser:

    def __init__(self, text):
        self.diagnostic_bag = DiagnosticBag()
        self._tokens = []
        self._position = 0
        self._lex(text)

    def parse(self):
        return self._parse()

    def _lex(self, text):
        lexer = Lexer(text)
        while True:
            token = lexer.lex_token()
            if (token.kind is SyntaxKind.WHITE_SPACE_TOKEN or
                    token.kind is SyntaxKind.BAD_TOKEN):
                continue
            else:
                self._tokens.append(token)

            if token.kind is SyntaxKind.END_OF_FILE_TOKEN:
                break
        self.diagnostic_bag.diagnostics.extend(lexer.diagnostic_bag.diagnostics)

    def _reset(self):
        self.diagnostic_bag.diagnostics.clear()
        self._tokens.clear()

    def _peek(self, offset):
        index = self._position + offset
        if index >= len(self._tokens):
            return self._tokens[len(self._tokens) - 1]
        else:
            return self._tokens[index]

    def _current(self):
        return self._peek(0)

    def _lookahead(self):
        return self._peek(1)

    def _next_token(self):
        current = self._current()
        self._position += 1
        return current

    def _match_token(self, kind):
        if self._current().kind == kind:
            return self._next_token()
        else:
            self.diagnostic_bag.report_unexpected_token(
                self._current().text_span,
                self._current().kind,
                kind,
                logging.ERROR
            )
            return SyntaxToken(kind, self._current().position, '', None)

    def _parse_binary_expression(self, parent_precedence=0):
        unary_operator_precedence = self._current().kind.get_unary_operator_precedence()
        if (unary_operator_precedence != 0
                and unary_operator_precedence >= parent_precedence):
            operator_token = self._next_token()
            operand = self._parse_binary_expression(unary_operator_precedence)
            left = UnaryExpressionSyntax(operator_token, operand)
        else:
            left = self._parse_primary_expression()

        while True:
            binary_operator_precedence = self._current().kind.get_binary_operator_precedence()
            if (binary_operator_precedence == 0 or
                    binary_operator_precedence <= parent_precedence):
                break
            else:
                operator_token = self._next_token()
                right = self._parse_binary_expression(binary_operator_precedence)
                left = BinaryExpressionSyntax(left, operator_token, right)
        return left

    def _parse_assignment_expression(self):
        # a + b + 5
        #
        #       +
        #      / \
        #     +   5
        #    / \
        #   a   b
        #
        # a = b = 5
        #
        #    =
        #   / \
        #  a   =
        #     / \
        #    b   5
        if (self._current().kind is SyntaxKind.IDENTIFIER_TOKEN and
                self._lookahead().kind is SyntaxKind.EQUALS_TOKEN):
            identifier_token = self._next_token()
            equals_token = self._next_token()
            right = self._parse_assignment_expression()
            return AssignmentExpressionSyntax(identifier_token, equals_token, right)
        else:
            return self._parse_binary_expression()

    def _parse_expression(self):
        return self._parse_assignment_expression()

    def _parse_primary_expression(self):

        def parse_parenthesized_expression():
            left = self._next_token()
            expression = self._parse_expression()
            right = self._match_token(SyntaxKind.CLOSE_PARENTHESIS_TOKEN)
            return ParenthesizedExpressionSyntax(left, expression, right)

        def parse_boolean_expression():
            keyword_token = self._next_token()
            value = keyword_token.kind is SyntaxKind.TRUE_KEYWORD
            return LiteralExpressionSyntax(keyword_token, value)

        def parse_name_expression():
            identifier_token = self._next_token()
            return NameExpressionSyntax(identifier_token)

        def parse_number_token():
            number_token = self._match_token(SyntaxKind.NUMBER_TOKEN)
            return LiteralExpressionSyntax(number_token)

        if (self._current().kind is SyntaxKind.TRUE_KEYWORD or
                self._current().kind is SyntaxKind.FALSE_KEYWORD):
            return parse_boolean_expression()
        elif self._current().kind is SyntaxKind.OPEN_PARENTHESIS_TOKEN:
            return parse_parenthesized_expression()
        elif self._current().kind is SyntaxKind.IDENTIFIER_TOKEN:
            return parse_name_expression()
        else:
            return parse_number_token()

    def _parse(self):
        expression = self._parse_expression()
        end_of_file_token = self._match_token(SyntaxKind.END_OF_FILE_TOKEN)
        return SyntaxTree(expression, self.diagnostic_bag, end_of_file_token)


class SyntaxTree:

    def __init__(self, expression_syntax, diagnostic_bag, end_of_file_token):
        self.diagnostic_bag = diagnostic_bag
        self.root = expression_syntax
        self.end_of_file_token = end_of_file_token

    @staticmethod
    def parse(text):
        parser = Parser(text)
        return parser.parse()

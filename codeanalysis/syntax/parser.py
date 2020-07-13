import logging

from .binary_expression_syntax import BinaryExpressionSyntax
from .lexer import Lexer
from .syntax_kind import SyntaxKind
from .literal_expression_syntax import LiteralExpressionSyntax
from .parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from .syntax_token import SyntaxToken
from .unary_expression_syntax import UnaryExpressionSyntax


class Parser:

    def __init__(self, text, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.diagnostics = []
        self._tokens = []
        self._position = 0
        self._lex(text)

    def parse(self):
        return self._parse()

    def _lex(self, text):
        lexer = Lexer(text)
        while True:
            token = lexer.lex_token()
            if token.kind is SyntaxKind.WHITE_SPACE_TOKEN or token.kind is SyntaxKind.BAD_TOKEN:
                continue
            else:
                self._tokens.append(token)

            if token.kind is SyntaxKind.END_OF_FILE_TOKEN:
                break
        self.diagnostics.extend(lexer.diagnostics)

    def _reset(self):
        self.diagnostics.clear()
        self._tokens.clear()

    def _peek(self, offset):
        index = self._position + offset
        if index >= len(self._tokens):
            return self._tokens[len(self._tokens) - 1]
        else:
            return self._tokens[index]

    def _current(self):
        return self._peek(0)

    def _next_token(self):
        current = self._current()
        self._position += 1
        return current

    def _match_token(self, kind):
        if self._current().kind == kind:
            return self._next_token()
        else:
            self.diagnostics.append(
                (
                    f"""Unexpected token '{self._current().kind}', expected '{kind}'""",
                    logging.ERROR
                )
            )
            return SyntaxToken(kind, self._current().position, None, None)

    def _parse_expression(self, parent_precedence=0):
        unary_operator_precedence = self._current().kind.get_unary_operator_precedence()
        if unary_operator_precedence != 0 and unary_operator_precedence >= parent_precedence:
            operator_token = self._next_token()
            operand = self._parse_expression(unary_operator_precedence)
            left = UnaryExpressionSyntax(operator_token, operand)
        else:
            left = self._parse_primary_expression()

        while True:
            binary_operator_precedence = self._current().kind.get_binary_operator_precedence()
            if binary_operator_precedence == 0 or binary_operator_precedence <= parent_precedence:
                break
            else:
                operator_token = self._next_token()
                right = self._parse_expression(binary_operator_precedence)
                left = BinaryExpressionSyntax(left, operator_token, right)
        return left

    def _parse_primary_expression(self):
        if self._current().kind is SyntaxKind.OPEN_PARENTHESIS_TOKEN:
            left = self._next_token()
            expression = self._parse_expression()
            right = self._match_token(SyntaxKind.CLOSE_PARENTHESIS_TOKEN)
            return ParenthesizedExpressionSyntax(
                left,
                expression,
                right
            )
        elif self._current().kind is SyntaxKind.TRUE_KEYWORD or self._current().kind is SyntaxKind.FALSE_KEYWORD:
            keyword_token = self._next_token()
            value = keyword_token.kind is SyntaxKind.TRUE_KEYWORD
            return LiteralExpressionSyntax(keyword_token, value)
        else:
            number_token = self._match_token(SyntaxKind.NUMBER_TOKEN)
            return LiteralExpressionSyntax(number_token)

    def _parse(self):
        expression = self._parse_expression()
        end_of_file_token = self._match_token(SyntaxKind.END_OF_FILE_TOKEN)
        return SyntaxTree(
            expression,
            self.diagnostics,
            end_of_file_token,
            self.logger
        )


class SyntaxTree:

    def __init__(self, expression_syntax, diagnostics, end_of_file_token, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.diagnostics = diagnostics
        self.root = expression_syntax
        self.end_of_file_token = end_of_file_token

    @staticmethod
    def parse(text, logger=None):
        logger = logger or logging.getLogger(__name__)
        parser = Parser(text, logger)
        return parser.parse()

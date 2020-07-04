import logging

from .lexer import Lexer
from .syntax import (
    SyntaxKind,
    SyntaxToken,
    NumberExpressionSyntax,
    BinaryExpressionSyntax,
    ParenthesizedExpressionSyntax
)


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
            token = lexer.next_token()
            if (token.syntaxkind != SyntaxKind.SpaceToken and
                    token.syntaxkind != token.syntaxkind.BadToken):
                self._tokens.append(token)
            if token.syntaxkind == SyntaxKind.EndOfFileToken:
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

    def _match(self, syntaxkind):
        if self._current().syntaxkind == syntaxkind:
            return self._next_token()
        else:
            self.diagnostics.append(
                (f"""Unexpected token '{self._current().syntaxkind}'', expected '{syntaxkind}'""", logging.ERROR))
            return SyntaxToken(syntaxkind, self._current().position, None, None)

    def _parse_expression(self):
        return self._parse_term()

    def _parse_primary_expression(self):
        if self._current().syntaxkind == SyntaxKind.OpenParenthesisToken:
            left = self._next_token()
            expression = self._parse_expression()
            right = self._match(SyntaxKind.CloseParenthesisToken)
            return ParenthesizedExpressionSyntax(left, expression, right)
        else:
            numbertoken = self._match(SyntaxKind.NumberToken)
            return NumberExpressionSyntax(numbertoken)

    def _parse_factor(self):
        left = self._parse_primary_expression()

        while (self._current().syntaxkind == SyntaxKind.StarToken or
               self._current().syntaxkind == SyntaxKind.SlashToken):
            operatortoken = self._next_token()
            right = self._parse_primary_expression()
            left = BinaryExpressionSyntax(left, operatortoken, right)

        return left

    def _parse_term(self):
        left = self._parse_factor()

        while (self._current().syntaxkind == SyntaxKind.PlusToken or
               self._current().syntaxkind == SyntaxKind.MinusToken):
            operatortoken = self._next_token()
            right = self._parse_factor()
            left = BinaryExpressionSyntax(left, operatortoken, right)

        return left

    def _parse(self):
        expression = self._parse_term()
        end_of_file_token = self._match(SyntaxKind.EndOfFileToken)
        return SyntaxTree(expression, self.diagnostics, end_of_file_token, self.logger)


class SyntaxTree:

    def __init__(self, expressionsyntax, diagnostics, end_of_file_token, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.diagnostics = diagnostics
        self.root = expressionsyntax
        self.end_of_file_token = end_of_file_token

    def has_diagnostics(self):
        return False if len(self.diagnostics) == 0 else True

    def report_diagnostics(self):
        for diagnostic, level in self.diagnostics:
            self.logger.log(level, diagnostic)

    @staticmethod
    def parse(text, logger=None):
        logger = logger or logging.getLogger(__name__)
        parser = Parser(text)
        return parser.parse()

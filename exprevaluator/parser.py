import logging

from .lexer import Lexer
from .syntax import (
    SyntaxKind,
    SyntaxToken,
    LiteralExpressionSyntax,
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
            token = lexer.lex_token()
            if (token.syntaxkind != SyntaxKind.WhiteSpaceToken and
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

    def _match_token(self, syntaxkind):
        if self._current().syntaxkind == syntaxkind:
            return self._next_token()
        else:
            self.diagnostics.append(
                (f"""Unexpected token '{self._current().syntaxkind}', expected '{syntaxkind}'""", logging.ERROR))
            return SyntaxToken(syntaxkind, self._current().position, None, None)

    def _get_binary_operator_precedence(self, syntaxkind):
        if (syntaxkind == SyntaxKind.StarToken or
                syntaxkind == SyntaxKind.SlashToken):
            return 2
        elif (syntaxkind == SyntaxKind.PlusToken or
                syntaxkind == SyntaxKind.MinusToken):
            return 1
        else:
            return 0

    def _parse_expression(self, parent_precedence=0):
        left = self._parse_primary_expression()
        while True:
            precedence = self._get_binary_operator_precedence(self._current().syntaxkind)
            if precedence == 0 or precedence <= parent_precedence:
                break
            else:
                operatortoken = self._next_token()
                right = self._parse_expression(precedence)
                left = BinaryExpressionSyntax(left, operatortoken, right)
        return left

    def _parse_primary_expression(self):
        if self._current().syntaxkind == SyntaxKind.OpenParenthesisToken:
            left = self._next_token()
            expression = self._parse_expression()
            right = self._match_token(SyntaxKind.CloseParenthesisToken)
            return ParenthesizedExpressionSyntax(left, expression, right)
        else:
            numbertoken = self._match_token(SyntaxKind.NumberToken)
            return LiteralExpressionSyntax(numbertoken)

    def _parse(self):
        expression = self._parse_expression()
        end_of_file_token = self._match_token(SyntaxKind.EndOfFileToken)
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
        parser = Parser(text, logger)
        return parser.parse()

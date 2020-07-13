import logging

from .syntax_token import SyntaxToken
from .syntax_kind import SyntaxKind


class Lexer:

    def __init__(self, text):
        self.diagnostics = []
        self.text = text
        self._position = 0

    def _peek(self, offset):
        index = self._position + offset
        if index >= len(self.text):
            return '\0'
        else:
            return self.text[index]

    def _current_char(self):
        return self._peek(0)

    def _lookahead(self):
        return self._peek(1)

    def _next(self, consume=1):
        self._position += consume

    def lex_token(self):
        start_position = self._position
        if self._current_char() == '\0':
            syntax_token = SyntaxToken(
                SyntaxKind.END_OF_FILE_TOKEN,
                start_position,
                '\0',
                None
            )
            return syntax_token
        elif self._current_char().isdigit():
            while self._current_char().isdigit():
                self._next()
            string = self.text[start_position:self._position]
            value = None
            try:
                value = int(string)
            except ValueError:
                self.diagnostics.append(
                    (
                        f'''The character/s '{string}' cannot be converted to integer''',
                        logging.ERROR
                    )
                )
            return SyntaxToken(
                SyntaxKind.NUMBER_TOKEN,
                start_position,
                string,
                value
            )
        elif self._current_char().isspace():
            while self._current_char().isspace():
                self._next()
            string = self.text[start_position:self._position]
            return SyntaxToken(
                SyntaxKind.WHITE_SPACE_TOKEN,
                start_position,
                string,
                None
            )
        elif self._current_char().isalpha():
            while self._current_char().isalpha():
                self._next()
            string = self.text[start_position:self._position]
            kind = SyntaxKind.get_keyword_kind(string)
            syntax_token = SyntaxToken(
                kind,
                start_position,
                string,
                None
            )
            return syntax_token
        elif self._current_char() == '+':
            self._next()
            return SyntaxToken(
                SyntaxKind.PLUS_TOKEN,
                start_position,
                '+',
                None
            )
        elif self._current_char() == '-':
            self._next()
            return SyntaxToken(
                SyntaxKind.MINUS_TOKEN,
                start_position,
                '-',
                None
            )
        elif self._current_char() == '*':
            self._next()
            return SyntaxToken(
                SyntaxKind.STAR_TOKEN,
                start_position,
                '*',
                None
            )
        elif self._current_char() == '/':
            self._next()
            return SyntaxToken(
                SyntaxKind.SLASH_TOKEN,
                start_position,
                '/',
                None
            )
        elif self._current_char() == '(':
            self._next()
            return SyntaxToken(
                SyntaxKind.OPEN_PARENTHESIS_TOKEN,
                start_position,
                '(',
                None
            )
        elif self._current_char() == ')':
            self._next()
            return SyntaxToken(
                SyntaxKind.CLOSE_PARENTHESIS_TOKEN,
                start_position,
                ')',
                None
            )
        elif self._current_char() == '=' and self._lookahead() == '=':
            self._next(2)
            return SyntaxToken(
                SyntaxKind.DOUBLE_EQUALS_TOKEN,
                start_position,
                '==',
                None
            )
        elif self._current_char() == '!' and self._lookahead() == '=':
            self._next(2)
            return SyntaxToken(
                SyntaxKind.BANG_EQUALS_TOKEN,
                start_position,
                '!=',
                None
            )
        elif self._current_char() == '&' and self._lookahead() == '&':
            self._next(2)
            return SyntaxToken(
                SyntaxKind.DOUBLE_AMPERSAND_TOKEN,
                start_position,
                '&&',
                None
            )
        elif self._current_char() == '|' and self._lookahead() == '|':
            self._next(2)
            return SyntaxToken(
                SyntaxKind.DOUBLE_PIPE_TOKEN,
                start_position,
                '||',
                None
            )
        elif self._current_char() == '!':
            self._next()
            return SyntaxToken(
                SyntaxKind.BANG_TOKEN,
                start_position,
                '!',
                None
            )
        else:
            string = self.text[start_position]
            self.diagnostics.append(
                (
                    f'''Bad character "{self._current_char()}" at position {start_position + 1}''',
                    logging.ERROR
                )
            )
            self._next()
            return SyntaxToken(
                SyntaxKind.BAD_TOKEN,
                start_position,
                string,
                None
            )

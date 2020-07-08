import logging

from .syntax_token import SyntaxToken
from .syntax_kind import SyntaxKind


class Lexer:

    def __init__(self, text):
        self.diagnostics = []
        self.text = text
        self._position = 0

    def _next(self):
        self._position += 1

    def _current_char(self):
        if self._position >= len(self.text):
            return '\0'
        else:
            return self.text[self._position]

    def lex_token(self):
        start_position = self._position

        if self._current_char() == '\0':
            return SyntaxToken(SyntaxKind.END_OF_FILE_TOKEN, start_position, '\0', None)

        elif self._current_char().isdigit():

            while self._current_char().isdigit():
                self._next()

            string = self.text[start_position:self._position]
            value = None
            try:
                value = int(string)
            except ValueError:
                self.diagnostics.append((f'''The character/s '{string}' cannot be converted to integer''',
                                         logging.ERROR))

            return SyntaxToken(SyntaxKind.NUMBER_TOKEN, start_position, string, value)

        elif self._current_char().isspace():

            while self._current_char().isspace():
                self._next()

            string = self.text[start_position:self._position]
            return SyntaxToken(SyntaxKind.WHITE_SPACE_TOKEN, start_position, string, None)

        elif self._current_char() == '+':
            self._next()
            return SyntaxToken(SyntaxKind.PLUS_TOKEN, start_position, '+', None)

        elif self._current_char() == '-':
            self._next()
            return SyntaxToken(SyntaxKind.MINUS_TOKEN, start_position, '-', None)

        elif self._current_char() == '*':
            self._next()
            return SyntaxToken(SyntaxKind.STAR_TOKEN, start_position, '*', None)

        elif self._current_char() == '/':
            self._next()
            return SyntaxToken(SyntaxKind.SLASH_TOKEN, start_position, '/', None)

        elif self._current_char() == '(':
            self._next()
            return SyntaxToken(SyntaxKind.OPEN_PARENTHESIS_TOKEN, start_position, '(', None)

        elif self._current_char() == ')':
            self._next()
            return SyntaxToken(SyntaxKind.CLOSE_PARENTHESIS_TOKEN, start_position, ')', None)

        else:
            string = self.text[start_position]
            self.diagnostics.append((f'''Bad character "{self._current_char()}" at position {start_position + 1}''',
                                     logging.ERROR))
            self._next()
            return SyntaxToken(SyntaxKind.BAD_TOKEN, start_position, string, None)

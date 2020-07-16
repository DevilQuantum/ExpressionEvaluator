from codeanalysis.text_span import TextSpan


class Diagnostic:

    def __init__(self, text_span, message, level):
        self.text_span = text_span
        self.message = message
        self.level = level

    def __str__(self):
        return self.message


class DiagnosticBag:

    def __init__(self):
        self.diagnostics = []

    def report(self, text_span, message, level):
        diagnostic = Diagnostic(text_span, message, level)
        self.diagnostics.append(diagnostic)

    def report_invalid_number(self, text_span, text, number_type, level):
        message = f"""The character/s '{text}' cannot be converted into {number_type}."""
        self.report(
            text_span,
            message,
            level
        )

    def report_bad_character(self, position, character, level):
        message = f"""Bad character '{character}' at position {position}."""
        self.report(
            TextSpan(position, 1),
            message,
            level
        ),

    def report_unexpected_token(self, text_span, kind, expected_kind, level):
        message = f'Unexpected token \"{kind}\", expected \"{expected_kind}\".'
        self.report(
            text_span,
            message,
            level
        )

    def report_undefined_unary_operator(self, text_span, text, operand_type, level):
        message = (
            f'Unary operator \"{text}\" is not defined for type '
            f'\"{operand_type}.\"'
        )
        self.report(
            text_span,
            message,
            level
        )

    def report_undefined_binary_operator(self, text_span, text, left_type, right_type, level):
        message = (
            f'Binary operator "{text}" is not defined for types '
            f'\"{left_type}\" and \"{right_type}\".'
        )
        self.report(
            text_span,
            message,
            level
        )

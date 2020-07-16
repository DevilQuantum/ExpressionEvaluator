class TextSpan:

    def __init__(self, start, length):
        self.start = start
        self.length = length
        self.end = start + length

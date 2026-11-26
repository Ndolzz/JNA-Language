from dataclasses import dataclass


KEYWORDS = {
    "ngomong",
    "takon",
    "nek",
    "liyane",
    "baleni",
    "gawe",
    "balekna",
    "bener",
    "salah",
    "kosong",
    "mandheg",
    "terusna",
    "ngaso",
    "ngunduh",
    "wis",
}


@dataclass
class Token:
    type: str
    value: object
    line: int
    column: int

    def __repr__(self):
        return (
            f"Token({self.type}, {self.value!r}, "
            f"line={self.line}, column={self.column})"
        )


class LexerError(Exception):
    pass


class Lexer:
    OPERATORS = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "STAR",
        "/": "SLASH",
        "%": "PERCENT",
        "=": "EQUAL",
        "==": "EQUAL_EQUAL",
        "!=": "NOT_EQUAL",
        "<": "LESS",
        ">": "GREATER",
        "<=": "LESS_EQUAL",
        ">=": "GREATER_EQUAL",
        "(": "LPAREN",
        ")": "RPAREN",
        "[": "LBRACKET",
        "]": "RBRACKET",
        "{": "LBRACE",
        "}": "RBRACE",
        ",": "COMMA",
        ":": "COLON",
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.line = 1
        self.column = 1
        self.indents = [0]

    def tokenize(self):
        lines = self.source.splitlines()

        for line_number, line in enumerate(lines, 1):
            self.line = line_number
            self.column = 1

            stripped = line.lstrip(" ")

            if not stripped or stripped.startswith("#"):
                continue

            indent = len(line) - len(stripped)

            if "\t" in line[:indent]:
                raise LexerError(
                    f"Tab indentation tidak diizinkan "
                    f"pada baris {line_number}"
                )

            if indent > self.indents[-1]:
                self.indents.append(indent)
                self.add("INDENT", indent, 1)

            elif indent < self.indents[-1]:
                while indent < self.indents[-1]:
                    self.indents.pop()
                    self.add("DEDENT", indent, 1)

                if indent != self.indents[-1]:
                    raise LexerError(
                        f"Indentasi tidak konsisten "
                        f"pada baris {line_number}"
                    )

            self.scan_line(line)
            self.add("NEWLINE", "\n", len(line) + 1)

        while len(self.indents) > 1:
            self.indents.pop()
            self.add("DEDENT", 0, 1)

        self.add("EOF", None, 1)

        return self.tokens

    def scan_line(self, line):
        i = 0

        while i < len(line):
            char = line[i]
            self.column = i + 1

            if char == " ":
                i += 1
                continue

            if char == "#":
                break

            if char in ("'", '"'):
                start = i
                value, i = self.read_string(line, i)
                self.add("STRING", value, start + 1)
                continue

            if char.isdigit():
                start = i
                value, i = self.read_number(line, i)
                self.add("NUMBER", value, start + 1)
                continue

            if char.isalpha() or char == "_":
                start = i
                value, i = self.read_identifier(line, i)

                token_type = (
                    "KEYWORD" if value in KEYWORDS
                    else "IDENTIFIER"
                )

                self.add(token_type, value, start + 1)
                continue

            operator = None

            for size in (2, 1):
                candidate = line[i:i + size]

                if candidate in self.OPERATORS:
                    operator = candidate
                    break

            if operator:
                self.add(
                    self.OPERATORS[operator],
                    operator,
                    i + 1
                )
                i += len(operator)
                continue

            raise LexerError(
                f"Karakter tidak dikenal {char!r} "
                f"pada baris {self.line}, kolom {i + 1}"
            )

        if self.column < len(line) + 1:
            self.column = len(line) + 1

    def read_string(self, line, start):
        quote = line[start]
        i = start + 1
        result = []

        while i < len(line):
            char = line[i]

            if char == quote:
                return "".join(result), i + 1

            if char == "\\":
                i += 1

                if i >= len(line):
                    break

                escapes = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    "'": "'",
                    '"': '"',
                }

                result.append(escapes.get(line[i], line[i]))

            else:
                result.append(char)

            i += 1

        raise LexerError(
            f"String tidak ditutup pada baris {self.line}"
        )

    def read_number(self, line, start):
        i = start

        while i < len(line) and line[i].isdigit():
            i += 1

        if (
            i + 1 < len(line)
            and line[i] == "."
            and line[i + 1].isdigit()
        ):
            i += 1

            while i < len(line) and line[i].isdigit():
                i += 1

            return float(line[start:i]), i

        return int(line[start:i]), i

    def read_identifier(self, line, start):
        i = start

        while i < len(line):
            char = line[i]

            if char.isalnum() or char == "_":
                i += 1
            else:
                break

        return line[start:i], i

    def add(self, token_type, value, column):
        self.tokens.append(
            Token(
                token_type,
                value,
                self.line,
                column
            )
        )


def tokenize(source):
    return Lexer(source).tokenize()

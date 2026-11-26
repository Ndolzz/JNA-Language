from dataclasses import dataclass


# AST NODES

@dataclass
class Program:
    statements: list


@dataclass
class Number:
    value: object


@dataclass
class String:
    value: str


@dataclass
class Boolean:
    value: bool


@dataclass
class Null:
    pass


@dataclass
class Variable:
    name: str


@dataclass
class Binary:
    left: object
    operator: str
    right: object


@dataclass
class Unary:
    operator: str
    operand: object


@dataclass
class Assignment:
    name: str
    value: object


@dataclass
class Print:
    value: object


@dataclass
class If:
    condition: object
    body: list
    otherwise: list


@dataclass
class Repeat:
    count: object
    body: list


@dataclass
class FunctionDef:
    name: str
    params: list
    body: list
    line: int = 0


@dataclass
class Return:
    value: object = None
    line: int = 0


@dataclass
class Call:
    name: str
    arguments: list
    line: int = 0


@dataclass
class ExpressionStatement:
    expression: object


@dataclass
class Break:
    line: int = 0


@dataclass
class Continue:
    line: int = 0


@dataclass
class Takon:
    prompt: object = None
    line: int = 0


@dataclass
class Ngaso:
    duration: object
    line: int = 0


@dataclass
class ListLiteral:
    items: list


@dataclass
class Index:
    target: object
    index: object


@dataclass
class Interpolation:
    parts: list


@dataclass
class DictLiteral:
    pairs: list


@dataclass
class IndexAssign:
    name: str
    index: object
    value: object


@dataclass
class Ngunduh:
    path: object
    line: int = 0


@dataclass
class End:
    pass


class ParserError(Exception):
    pass


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def peek(self):
        next_position = self.position + 1

        if next_position < len(self.tokens):
            return self.tokens[next_position]

        return self.tokens[-1]

    def advance(self):
        token = self.current()
        if token.type != "EOF":
            self.position += 1
        return token

    def match(self, *types):
        if self.current().type in types:
            return self.advance()
        return None

    def expect(self, token_type):
        token = self.current()

        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type}, got {token.type} "
                f"at line {token.line}"
            )

        return self.advance()

    def skip_newlines(self):
        while self.match("NEWLINE"):
            pass

    def parse(self):
        statements = []

        self.skip_newlines()

        while self.current().type != "EOF":
            statements.append(self.statement())
            self.skip_newlines()

        return Program(statements)

    def statement(self):
        token = self.current()

        if token.type == "IDENTIFIER":
            if self.peek().type == "LPAREN":
                self.advance()
                expression = self.finish_call(token)
                return ExpressionStatement(expression)

            if self.peek().type == "LBRACKET":
                return self.index_assignment()

            return self.assignment()

        if token.type == "KEYWORD":
            if token.value == "ngomong":
                return self.print_statement()

            if token.value == "nek":
                return self.if_statement()

            if token.value == "baleni":
                return self.repeat_statement()

            if token.value == "gawe":
                return self.function_statement()

            if token.value == "balekna":
                return self.return_statement()

            if token.value == "mandheg":
                return self.break_statement()

            if token.value == "terusna":
                return self.continue_statement()

            if token.value == "ngaso":
                return self.ngaso_statement()

            if token.value == "ngunduh":
                self.advance()
                path = self.expression()
                return Ngunduh(path, token.line)

            if token.value == "wis":
                self.advance()
                return End()

        raise ParserError(
            f"Unexpected token {token.value!r} "
            f"at line {token.line}"
        )

    def assignment(self):
        name = self.expect("IDENTIFIER").value
        self.expect("EQUAL")
        value = self.expression()

        return Assignment(name, value)

    def print_statement(self):
        self.expect("KEYWORD")
        value = self.expression()

        return Print(value)

    def if_statement(self):
        self.expect("KEYWORD")

        condition = self.expression()

        self.expect("COLON")
        self.expect("NEWLINE")

        body = self.block()
        otherwise = []

        if (
            self.current().type == "KEYWORD"
            and self.current().value == "liyane"
        ):
            self.advance()
            self.expect("COLON")
            self.expect("NEWLINE")
            otherwise = self.block()

        return If(condition, body, otherwise)

    def repeat_statement(self):
        self.expect("KEYWORD")

        count = self.expression()

        self.expect("COLON")
        self.expect("NEWLINE")

        body = self.block()

        return Repeat(count, body)

    def function_statement(self):
        token = self.expect("KEYWORD")
        name = self.expect("IDENTIFIER").value
        self.expect("LPAREN")

        params = []

        if self.current().type != "RPAREN":
            params.append(self.expect("IDENTIFIER").value)

            while self.match("COMMA"):
                params.append(self.expect("IDENTIFIER").value)

        self.expect("RPAREN")
        self.expect("COLON")
        self.expect("NEWLINE")

        body = self.block()

        if len(params) != len(set(params)):
            raise ParserError(
                f"Parameter duplikat pada fungsi '{name}' "
                f"at line {token.line}"
            )

        return FunctionDef(name, params, body, token.line)

    def break_statement(self):
        token = self.expect("KEYWORD")
        return Break(token.line)

    def continue_statement(self):
        token = self.expect("KEYWORD")
        return Continue(token.line)

    def return_statement(self):
        token = self.expect("KEYWORD")

        value = None

        if self.current().type not in ("NEWLINE", "DEDENT", "EOF"):
            value = self.expression()

        return Return(value, token.line)

    def ngaso_statement(self):
        token = self.expect("KEYWORD")
        duration = self.expression()

        return Ngaso(duration, token.line)

    def index_assignment(self):
        name = self.expect("IDENTIFIER").value
        self.expect("LBRACKET")
        index = self.expression()
        self.expect("RBRACKET")
        self.expect("EQUAL")
        value = self.expression()

        return IndexAssign(name, index, value)

    def block(self):
        self.expect("INDENT")

        statements = []
        self.skip_newlines()

        while self.current().type not in ("DEDENT", "EOF"):
            statements.append(self.statement())
            self.skip_newlines()

        self.expect("DEDENT")

        return statements

    # EXPRESSION PARSER

    def expression(self):
        return self.comparison()

    def comparison(self):
        left = self.addition()

        operators = (
            "EQUAL_EQUAL",
            "NOT_EQUAL",
            "LESS",
            "GREATER",
            "LESS_EQUAL",
            "GREATER_EQUAL",
        )

        while self.current().type in operators:
            operator = self.advance()
            right = self.addition()

            left = Binary(left, operator.type, right)

        return left

    def addition(self):
        left = self.multiplication()

        while self.current().type in ("PLUS", "MINUS"):
            operator = self.advance()
            right = self.multiplication()

            left = Binary(left, operator.type, right)

        return left

    def multiplication(self):
        left = self.unary()

        while self.current().type in (
            "STAR", "SLASH", "PERCENT"
        ):
            operator = self.advance()
            right = self.unary()

            left = Binary(left, operator.type, right)

        return left

    def unary(self):
        if self.current().type in ("MINUS",):
            operator = self.advance()
            return Unary(operator.type, self.unary())

        return self.postfix()

    def build_string(self, token):
        if "{" not in token.value and "}" not in token.value:
            return String(token.value)

        return self.build_interpolation(token.value, token.line)

    def build_interpolation(self, text, line):
        parts = []
        literal = []
        i = 0

        while i < len(text):
            char = text[i]

            if char == "{":
                if i + 1 < len(text) and text[i + 1] == "{":
                    literal.append("{")
                    i += 2
                    continue

                if literal:
                    parts.append("".join(literal))
                    literal = []

                end = text.find("}", i + 1)

                if end == -1:
                    raise ParserError(
                        f"Kurung pembuka '{{' durung ditutup "
                        f"nang string pada baris {line}"
                    )

                name = text[i + 1:end].strip()

                if not self.is_identifier(name):
                    raise ParserError(
                        f"'{name}' dudu jeneng variabel sing sah "
                        f"nang string pada baris {line}"
                    )

                parts.append(Variable(name))
                i = end + 1

            elif char == "}":
                if i + 1 < len(text) and text[i + 1] == "}":
                    literal.append("}")
                    i += 2
                    continue

                raise ParserError(
                    f"Kurung penutup '}}' sing ora pas "
                    f"nang string pada baris {line}"
                )

            else:
                literal.append(char)
                i += 1

        if literal:
            parts.append("".join(literal))

        if len(parts) == 1 and isinstance(parts[0], str):
            return String(parts[0])

        return Interpolation(parts)

    @staticmethod
    def is_identifier(name):
        if not name:
            return False

        if not (name[0].isalpha() or name[0] == "_"):
            return False

        return all(ch.isalnum() or ch == "_" for ch in name)

    def postfix(self):
        value = self.primary()

        while self.current().type == "LBRACKET":
            self.advance()
            index = self.expression()
            self.expect("RBRACKET")
            value = Index(value, index)

        return value

    def primary(self):
        token = self.current()

        if self.match("NUMBER"):
            return Number(token.value)

        if self.match("STRING"):
            return self.build_string(token)

        if self.match("IDENTIFIER"):
            if self.current().type == "LPAREN":
                return self.finish_call(token)

            return Variable(token.value)

        if token.type == "KEYWORD":
            if token.value == "bener":
                self.advance()
                return Boolean(True)

            if token.value == "salah":
                self.advance()
                return Boolean(False)

            if token.value == "kosong":
                self.advance()
                return Null()

            if token.value == "takon":
                self.advance()

                prompt = None

                if self.current().type == "STRING":
                    prompt = self.build_string(self.advance())

                return Takon(prompt, token.line)

        if self.match("LBRACE"):
            pairs = []

            if self.current().type != "RBRACE":
                while True:
                    key = self.expression()
                    self.expect("COLON")
                    value = self.expression()
                    pairs.append([key, value])

                    if not self.match("COMMA"):
                        break

            self.expect("RBRACE")
            return DictLiteral(pairs)

        if self.match("LBRACKET"):
            items = []

            if self.current().type != "RBRACKET":
                items.append(self.expression())

                while self.match("COMMA"):
                    items.append(self.expression())

            self.expect("RBRACKET")
            return ListLiteral(items)

        if self.match("LPAREN"):
            value = self.expression()
            self.expect("RPAREN")
            return value

        raise ParserError(
            f"Invalid expression {token.value!r} "
            f"at line {token.line}"
        )

    def finish_call(self, name_token):
        self.expect("LPAREN")

        arguments = []

        if self.current().type != "RPAREN":
            arguments.append(self.expression())

            while self.match("COMMA"):
                arguments.append(self.expression())

        self.expect("RPAREN")

        return Call(name_token.value, arguments, name_token.line)


def parse(tokens):
    return Parser(tokens).parse()

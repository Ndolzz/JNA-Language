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

    def return_statement(self):
        token = self.expect("KEYWORD")

        value = None

        if self.current().type not in ("NEWLINE", "DEDENT", "EOF"):
            value = self.expression()

        return Return(value, token.line)

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

        return self.primary()

    def primary(self):
        token = self.current()

        if self.match("NUMBER"):
            return Number(token.value)

        if self.match("STRING"):
            return String(token.value)

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

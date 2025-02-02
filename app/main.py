import sys
import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def expression(self):
        return self.primary()

    def primary(self):
        if self.match("TRUE"):
            return Literal(True)
        if self.match("FALSE"):
            return Literal(False)
        if self.match("NIL"):
            return Literal(None)
        if self.match("NUMBER"):
            return Literal(self.previous().literal)
        if self.match("STRING"):
            return Literal(self.previous().literal)
        # Handle other literals and expressions...

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

class Expr:
    def accept(self, visitor):
        pass

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class AstPrinter:
    def print(self, expr):
        return expr.accept(self)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        if expr.value is True:
            return "true"
        if expr.value is False:
            return "false"
        return str(expr.value)

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        builder = []

        builder.append("(")
        builder.append(name)
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
        builder.append(")")

        return "".join(builder)

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

def extract_word(sentence, start_index):
    end_index = start_index
    while end_index < len(sentence) and (sentence[end_index].isalnum() or sentence[end_index] == "_"):
        end_index += 1
    return sentence[start_index:end_index]

def tokenize(file_contents):
    tokens = []
    i = 0
    keywords = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]
    while i < len(file_contents):
        x = file_contents[i]
        if x in [" ", "\t", "\n"]:
            i += 1
            continue
        elif x.isalpha() or x == "_":
            lit = extract_word(file_contents, i)
            if lit in keywords:
                tokens.append(Token(lit.upper(), lit, null, 1))
            else:
                tokens.append(Token("IDENTIFIER", lit, null, 1))
            i += len(lit)
            continue
        elif x.isdigit():
            match = re.match(r'\d+(\.\d+)?', file_contents[i:])
            if match:
                number_value = match.group()
                tokens.append(Token("NUMBER", number_value, float(number_value), 1))
                i += len(number_value)
                continue
        elif x == '"':
            end_index = file_contents.find('"', i + 1)
            if end_index == -1:
                line_number = file_contents.count("\n", 0, i) + 1
                print(
                    "[line %s] Error: Unterminated string." % (line_number),
                    file=sys.stderr
                )
                error = True
                break
            else:
                string_value = file_contents[i:end_index + 1]
                tokens.append(Token("STRING", string_value, string_value.strip("\""), 1))
                i = end_index + 1
                continue
        elif x == "/":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "/":
                # Skip the rest of the line for single-line comments
                while i < len(file_contents) and file_contents[i] != "\n":
                    i += 1
            else:
                tokens.append(Token("SLASH", "/", null, 1))
        elif x == "=":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("EQUAL_EQUAL", "==", null, 1))
                i += 1
            else:
                tokens.append(Token("EQUAL", "=", null, 1))
        elif x == "!":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("BANG_EQUAL", "!=", null, 1))
                i += 1
            else:
                tokens.append(Token("BANG", "!", null, 1))
        elif x == "<":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("LESS_EQUAL", "<=", null, 1))
                i += 1
            else:
                tokens.append(Token("LESS", "<", null, 1))
        elif x == ">":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("GREATER_EQUAL", ">=", null, 1))
                i += 1
            else:
                tokens.append(Token("GREATER", ">", null, 1))
        elif x == "(":
            tokens.append(Token("LEFT_PAREN", "(", null, 1))
        elif x == ")":
            tokens.append(Token("RIGHT_PAREN", ")", null, 1))
        elif x == "{":
            tokens.append(Token("LEFT_BRACE", "{", null, 1))
        elif x == "}":
            tokens.append(Token("RIGHT_BRACE", "}", null, 1))
        elif x == "*":
            tokens.append(Token("STAR", "*", null, 1))
        elif x == ".":
            tokens.append(Token("DOT", ".", null, 1))
        elif x == ",":
            tokens.append(Token("COMMA", ",", null, 1))
        elif x == "+":
            tokens.append(Token("PLUS", "+", null, 1))
        elif x == "-":
            tokens.append(Token("MINUS", "-", null, 1))
        elif x == ";":
            tokens.append(Token("SEMICOLON", ";", null, 1))
        else:
            error = True
            line_number = file_contents.count("\n", 0, i) + 1
            print(
                "[line %s] Error: Unexpected character: %s" % (line_number, x),
                file=sys.stderr,
            )
        i += 1
    tokens.append(Token("EOF", "", null, 1))
    return tokens

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    if command == "tokenize":
        tokens = tokenize(file_contents)
        for token in tokens:
            print(token)
    elif command == "parse":
        tokens = tokenize(file_contents)
        parser = Parser(tokens)
        expression = parser.parse()

        # Print the AST
        printer = AstPrinter()
        print(printer.print(expression))

if __name__ == "__main__":
    main()


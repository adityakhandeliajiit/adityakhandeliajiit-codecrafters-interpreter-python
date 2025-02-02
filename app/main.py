import sys
import re
class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.current=0
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
    def match(self,*types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
            else:
                return False
    def check(self,type):
        if self.is_at_end():
            return False
        return self.peek().type==type
    def advance(self):
        if not self.is_at_end():
            self.current+=1
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
def extract_word(sentence, start_index):
    end_index = start_index
    while end_index < len(sentence) and (sentence[end_index].isalnum() or sentence[end_index] == "_"):
        end_index += 1
    return sentence[start_index:end_index]

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize","parse"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    
    with open(filename) as file:
        file_contents = file.read()
    if command == "tokenize":
        pass
    elif command == "parse":
        tokens = []
        
        parser = Parser(tokens)
        expression = parser.parse()

        # Print the AST
        printer = AstPrinter()
        print(printer.print(expression))    

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    error = False
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
                print(f'{lit.upper()} {lit} null')
            else:
                print(f'IDENTIFIER {lit} null')
            i += len(lit)
            continue
        elif x.isdigit():
            match = re.match(r'\d+(\.\d+)?', file_contents[i:])
            if match:
                number_value = match.group()
                print(f"NUMBER {number_value} {float(number_value)}")
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
                print(f'STRING {string_value} {string_value.strip("\"")}')
                i = end_index + 1
                continue
        elif x == "/":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "/":
                # Skip the rest of the line for single-line comments
                while i < len(file_contents) and file_contents[i] != "\n":
                    i += 1
            else:
                print("SLASH / null")
        elif x == "=":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("EQUAL_EQUAL == null")
                i += 1
            else:
                print("EQUAL = null")
        elif x == "!":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("BANG_EQUAL != null")
                i += 1
            else:
                print("BANG ! null")
        elif x == "<":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("LESS_EQUAL <= null")
                i += 1
            else:
                print("LESS < null")
        elif x == ">":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("GREATER_EQUAL >= null")
                i += 1
            else:
                print("GREATER > null")
        elif x == "(":
            print("LEFT_PAREN ( null")
        elif x == ")":
            print("RIGHT_PAREN ) null")
        elif x == "{":
            print("LEFT_BRACE { null")
        elif x == "}":
            print("RIGHT_BRACE } null")
        elif x == "*":
            print("STAR * null")
        elif x == ".":
            print("DOT . null")
        elif x == ",":
            print("COMMA , null")
        elif x == "+":
            print("PLUS + null")
        elif x == "-":
            print("MINUS - null")
        elif x == ";":
            print("SEMICOLON ; null")
        else:
            error = True
            line_number = file_contents.count("\n", 0, i) + 1
            print(
                "[line %s] Error: Unexpected character: %s" % (line_number, x),
                file=sys.stderr,
            )
        i += 1
    print("EOF  null")
    if error:
        exit(65)
    else:
        exit(0)

if __name__ == "__main__":
    main()


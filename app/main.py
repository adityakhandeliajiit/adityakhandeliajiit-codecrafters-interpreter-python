import sys
import re

# Global error flag.
had_error_parse = False
had_error_evaluate=False
class Enviroment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeError(f"Undefined variable '{name}'.")
class BlockStmt:
    def __init__(self,statement):
        self.statement=statement
    def accept(self,visitor):
        return visitor.visit_block_stmt(self)    
class assignment:
    def __init__(self,name,value):
        self.name=name
        self.value=value
    def accept(self,visitor):
        return visitor.visit_assign_expr(self)    
class Variable:
    def __init__(self, name):
        self.name = name  # a Token
    def accept(self, visitor):
        return visitor.visit_variable_expr(self)
class expr_statement:
    def __init__(self,expression):
        self.expression=expression
    def accept(self,visitor):
        return visitor.visit_expr_stmt(self)    
class print_stmt:
    def __init__(self,expr):
        self.expression=expr
    def accept(self,visitor):
        return visitor.visit_print_stmt(self)    
class vardec_stmt:
    def __init__(self,name,initializer):
        self.name=name
        self.initializer=initializer
    def accept(self,visitor):
        return visitor.visit_vardec_stmt(self)    
        
class Interpreter:
    def __init__(self,mode,enviroment):
        self.mode=mode
        self.enviroment={}
    def interpret(self,statements):
        for stmt in statements:
            self.execute(stmt)
    def accept(self,stmt):
        stmt.accept(self)     
    def execute(self,stmt):
        stmt.accept(self)       
    def evaluate(self,expr):
        return expr.accept(self)
    def visit_literal_expr(self,expr):
        return expr.value    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression) 
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)  
        if expr.operator.lexeme == "-":
            if  type(right)==bool or type(right)==str : 
             exit(70)  
            return -right
        elif expr.operator.lexeme == "!":
            return not right
        # For other unary operators, add more branches as needed.
        return None
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op = expr.operator.lexeme
        if op == "+":
            if  type(right)==bool  or type(left)==bool or (type(left)==str and type(right)!=str) or (type(right)==str and type(left)!=str): 
                exit(70)
            return left + right
        elif op == "-":
            if  type(right)==bool or type(right)==str or type(left)==bool or type(left)==str : 
                exit(70)
            return left - right
        elif op == "*":
            if  type(right)==bool or type(right)==str or type(left)==bool or type(left)==str : 
                exit(70)
            return left * right
        elif op == "/":
            if  type(right)==bool or type(right)==str or type(left)==bool or type(left)==str : 
             exit(70)
            return left / right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            if  type(right)==bool or type(right)==str or type(left)==bool or type(left)==str : 
                exit(70)
            return left < right
        elif op == "<=":
            if  type(right)==bool or type(right)==str or type(left)==bool or type(left)==str : 
                exit(70)
            return left <= right
        elif op == ">":
            if  type(right)==bool or type(right)==str or type(left)==bool or type(left)==str : 
                exit(70)
            return left > right
        elif op == ">=":
            if  type(right)==bool or type(right)==str or type(left)==bool or type(left)==str : 
                exit(70)
            return left >= right    
    def visit_print_stmt(self,stmt):
        value=self.evaluate(stmt.expression)
        print(self.formatted(value)) 
    def visit_expr_stmt(self, stmt):
        value=self.evaluate(stmt.expression)
        if self.mode=="evaluate":
            print(self.formatted(value))
    def visit_vardec_stmt(self,stmt):
        value=None
        if stmt.initializer is not None:
            value=self.evaluate(stmt.initializer)
        self.enviroment[stmt.name.lexeme]=value
    def visit_variable_expr(self, expr):
        if expr.name.lexeme in self.enviroment:
           return self.enviroment[expr.name.lexeme]
        else:
          exit(70)  
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        if expr.name.lexeme in self.enviroment:
            self.enviroment[expr.name.lexeme] = value
        else:
            exit(70)  
        return value   
    def visit_block_stmt(self,stmt):
        previous=self.enviroment
        self.enviroment=Enviroment(previous)
        for statement in stmt.statements:
            self.execute(statement)
        self.enviroment=previous    
    def formatted(self,value):
        if value is None:
            return "nil"
        if isinstance(value, float) and value.is_integer():
           return str(int(value))
        if isinstance(value,str) and value[0].isupper():
                return value.capitalize()   
        return str(value).lower()               
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        try:
            while not self.is_at_end():
                statements.append(self.statement())
            return statements
        except Exception as e:
            self.error(self.peek(), str(e))
            return None
    def assignment(self):
        expr=self.equal_equal()
        if self.match("EQUAL"):
            equals=self.previous()
            value=self.assignment()
            if isinstance(expr,Variable):
               return assignment(expr.name,value)
            else:
               self.error(equals,"Invalid assignment")
        return expr 
    def block(self):
       statements = []
       while not self.check("RIGHT_BRACE") and not self.is_at_end():
            statements.append(self.declaration()) 
       self.consume("RIGHT_BRACE", "Expected '}' after block.")
       return BlockStmt(statements)                 
    def statement(self):
        if self.match("PRINT"):
            return self.print_stmt()
        elif self.match("VAR"):
            return self.var_declaration()    
        else:
            return self.expr_stmt()
    def expr_stmt(self):
        expr=self.expression()
        if self.check("SEMICOLON"):
            self.advance()
        return   expr_statement(expr)          
    def print_stmt(self):
        expr=self.expression()
        self.consume("SEMICOLON","expected ';'")
        return print_stmt(expr) 
    def var_declaration(self):
        name=self.consume("IDENTIFIER","Expect variable name")
        initializer=None
        if self.match("EQUAL"):
            initializer=self.expression()
        self.consume("SEMICOLON","expect ;")
        return vardec_stmt(name,initializer)  
    def expression(self):
        return self.assignment()
    def equal_equal(self):
        expr=self.comparison()
        while self.match("EQUAL_EQUAL","BANG_EQUAL"):
            operator=self.previous()
            right=self.comparison()
            expr=Binary(expr,operator,right)
        return expr        
    def comparison(self):
        expr=self.addition()
        while self.match("LESS_EQUAL","GREATER_EQUAL","LESS","GREATER"):
            operator=self.previous()
            right=self.addition()   
            expr=Binary(expr,operator,right)
        return expr        
    def addition(self):
        expr=self.multiplication()
        while self.match("PLUS","MINUS"):
            operator=self.previous()
            right=self.multiplication()
            expr=Binary(expr,operator,right)
        return expr    
    def multiplication(self):
        expr = self.unary()
        while self.match("STAR", "SLASH"):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)   
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
            return Literal(self.previous().literal)  # Pass the literal value
        # Handle other literals and expressions...
        if self.match("IDENTIFIER"):
            return Variable(self.previous())

        if self.match("LEFT_PAREN"):
            expr=self.expression()
            if not self.match("RIGHT_PAREN"):
              raise Exception("Expected ')' after expression")
            return Grouping(expr)  
        raise Exception("Expected expression")

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
    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise Exception(message)    

    def error(self, token, message):
        print(f"[line {token.line}] Error at '{token.lexeme}': {message}", file=sys.stderr)
        return Exception()

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
        if isinstance(expr.value, str):
            return expr.value
        return str(expr.value)

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    def visit_expr_stmt(self, stmt):   
            return stmt.expression.accept(self)
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
        literal_str = "null" if self.literal is None else self.literal
        return f"{self.type} {self.lexeme} {literal_str}"

def extract_word(sentence, start_index):
    end_index = start_index
    while end_index < len(sentence) and (sentence[end_index].isalnum() or sentence[end_index] == "_"):
        end_index += 1
    return sentence[start_index:end_index]

def tokenize(file_contents):
    global had_error_parse  # Use the global error flag.
    tokens = []
    i = 0
    keywords = [
        "and", "class", "else", "false", "for", "fun", "if", "nil", "or",
        "print", "return", "super", "this", "true", "var", "while"
    ]
    while i < len(file_contents):
        x = file_contents[i]
        if x in [" ", "\t", "\n"]:
            i += 1
            continue
        elif x.isalpha() or x == "_":
            lit = extract_word(file_contents, i)
            if lit in keywords:
                tokens.append(Token(lit.upper(), lit, None, 1))
            else:
                tokens.append(Token("IDENTIFIER", lit, None, 1))
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
                print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
                had_error_parse = True
                break
            else:
                string_value = file_contents[i:end_index + 1]
                literal_value = string_value[1:-1]  # Remove surrounding quotes
                tokens.append(Token("STRING", string_value, literal_value, 1))
                i = end_index + 1
                continue
        elif x == "/":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "/":
                # Skip the rest of the line for single-line comments
                while i < len(file_contents) and file_contents[i] != "\n":
                    i += 1
            else:
                tokens.append(Token("SLASH", "/", None, 1))
        elif x == "=":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("EQUAL_EQUAL", "==", None, 1))
                i += 1
            else:
                tokens.append(Token("EQUAL", "=", None, 1))
        elif x == "!":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("BANG_EQUAL", "!=", None, 1))
                i += 1
            else:
                tokens.append(Token("BANG", "!", None, 1))
        elif x == "<":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("LESS_EQUAL", "<=", None, 1))
                i += 1
            else:
                tokens.append(Token("LESS", "<", None, 1))
        elif x == ">":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(Token("GREATER_EQUAL", ">=", None, 1))
                i += 1
            else:
                tokens.append(Token("GREATER", ">", None, 1))
        elif x == "(":
            tokens.append(Token("LEFT_PAREN", "(", None, 1))
        elif x == ")":
            tokens.append(Token("RIGHT_PAREN", ")", None, 1))
        elif x == "{":
            tokens.append(Token("LEFT_BRACE", "{", None, 1))
        elif x == "}":
            tokens.append(Token("RIGHT_BRACE", "}", None, 1))
        elif x == "*":
            tokens.append(Token("STAR", "*", None, 1))
        elif x == ".":
            tokens.append(Token("DOT", ".", None, 1))
        elif x == ",":
            tokens.append(Token("COMMA", ",", None, 1))
        elif x == "+":
            tokens.append(Token("PLUS", "+", None, 1))
        elif x == "-":
            tokens.append(Token("MINUS", "-", None, 1))
        elif x == ";":
            tokens.append(Token("SEMICOLON", ";", None, 1))
        else:
            line_number = file_contents.count("\n", 0, i) + 1
            print(f"[line {line_number}] Error: Unexpected character: {x}", file=sys.stderr)
            had_error_parse = True  # Mark error when unexpected character is found.
        i += 1
    tokens.append(Token("EOF", "", None, 1))
    return tokens

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse","evaluate","run"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    tokens = tokenize(file_contents)
    if command == "tokenize":
        for token in tokens:
            print(token)
        if had_error_parse:
            exit(65)
    elif command == "parse":
        parser = Parser(tokens)
        if had_error_parse:
            exit(65)
        expression = parser.parse()
        if expression is None:
            exit(65)
        # Print the AST
        printer = AstPrinter()
        for stmt in expression:
             result = printer.print(stmt)
             print(result)
    elif command=="evaluate" or command=="run":
        tokens = tokenize(file_contents)
        parser = Parser(tokens)
        expression = parser.parse()
        if expression is None:
          exit(65)
        enviroment={}  
        if command=="evaluate":
            interpreter=Interpreter("evaluate",enviroment)
            interpreter.interpret(expression)
        elif command=="run":
            interpreter=Interpreter("run",enviroment)
            interpreter.interpret(expression)   


if __name__ == "__main__":
    main()

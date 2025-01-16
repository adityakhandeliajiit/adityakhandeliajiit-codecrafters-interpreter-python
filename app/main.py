import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    error=False
    for x in file_contents:
        if x == "(":
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
        elif x=="-":
            print("MINUS - null")
        elif x==";":
            print("SEMICOLON ; null")
        else:
            error = True
            line_number = file_contents.count("\n", 0, file_contents.find(x)) + 1
            print(
                "[line %s] Error: Unexpected character: %s" % (line_number,x),
                file=sys.stderr,
            )
    if error:
        exit(65)
    else:
        exit(0)                  
    print("EOF  null")
if __name__ == "__main__":
    main()


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
    print("EOF  null")
    # for line in file_contents:
    #         for char in line:
    #             match char:
    #                 case "(":
    #                     token = "LEFT_PAREN"
    #                 case ")":
    #                     token = "RIGHT_PAREN"
    #                 case "{":
    #                     token = "LEFT_BRACE"
    #                 case "}":
    #                     token = "RIGHT_BRACE"
    #                 case ",":
    #                     token = "COMMA"
    #                 case ".":
    #                     token = "DOT"
    #                 case "-":
    #                     token = "MINUS"
    #                 case "+":
    #                     token = "PLUS"
    #                 case ";":
    #                     token = "SEMICOLON"
    #                 case "*":
    #                     token = "STAR"
    #                 case _:
    #                     continue
    #                     # token = ""
    #             print(f"{token} {char} null")
    # print("EOF  null")


if __name__ == "__main__":
    main()


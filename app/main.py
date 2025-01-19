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
    error = False
    i = 0
    while i < len(file_contents):
        x = file_contents[i]
        if x=="/":
            if i+1<len(file_contents) and file_contents[i+1]=="/":
                #  print("EQUAL_EQUAL == null")
                #  i += 1
                # exit(0)
                break  
            else:
                print("SLASH / null")
        elif x=="=":
            if i+1<len(file_contents) and file_contents[i+1]=="=":
                 print("EQUAL_EQUAL == null")
                 i += 1  
            else:
                print("EQUAL = null")
        elif x=="!":
            if i+1<len(file_contents) and file_contents[i+1]=="=":
                 print("BANG_EQUAL != null")
                 i += 1  
            else: 
                print("BANG ! null")   
        elif x=="<":
            if i+1<len(file_contents) and file_contents[i+1]=="=":
                 print("LESS_EQUAL <= null")
                 i += 1  
            else: 
                print("LESS < null")
        elif x==">":
            if i+1<len(file_contents) and file_contents[i+1]=="=":
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
        elif x in [" ","\t"]:
            pass    
        else:
            error = True
            line_number = file_contents.count("\n", 0, file_contents.find(x)) + 1
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


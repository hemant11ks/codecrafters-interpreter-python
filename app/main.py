from ctypes import pointer
import sys


def findlinenum(file, char, pointer):
    #Find line of err
    line_num = file.count("\n", 0, file.find(char, pointer - 1)) + 1
    return line_num

def checkString(startIdx, file_contents, pointer):
    pointer = 0
    str = []
    while c != '"':
        pointer += 1
        c = file_contents[pointer]
        str.append(c)

    return 0

def checkNeighbor(file_contents, pointer, c):
    if c == "/":
        if (pointer + 1 < len(file_contents)) and file_contents[pointer + 1] == "/":
            return "EOF  null"
        else:
            return "SLASH / null"

    if (pointer + 1 < len(file_contents)) and file_contents[pointer + 1] == "=":
        pointer += 1
        if c == "=":
            return "EQUAL_EQUAL == null"
        if c == "!":
            return "BANG_EQUAL != null"
        if c == "<":
            return "LESS_EQUAL <= null"
        if c == ">":
            return "GREATER_EQUAL >= null"
    else:
        if c == "=":
            return "EQUAL = null"
        if c == "!":
            return "BANG ! null"
        if c == "<":
            return "LESS < null"
        if c == ">":
            return "GREATER > null"


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

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

    err = False
    pointer = 0
    while pointer < len(file_contents):
        c = file_contents[pointer]
        pointer += 1
        if c == "(":
            print("LEFT_PAREN ( null")
        elif c == ")":
            print("RIGHT_PAREN ) null")
        elif c == "{":
            print("LEFT_BRACE { null")
        elif c == "}":
            print("RIGHT_BRACE } null")
        elif c == "*":
            print("STAR * null")
        elif c == ".":
            print("DOT . null")
        elif c == ",":
            print("COMMA , null")
        elif c == "+":
            print("PLUS + null")
        elif c == "-":
            print("MINUS - null")
        elif c == ";":
            print("SEMICOLON ; null")
        elif c == "=":
            result = checkNeighbor(file_contents, pointer - 1, c)
            if result == "EQUAL_EQUAL == null":
                pointer += 1
            print(result)
        elif c == "!":
            result = checkNeighbor(file_contents, pointer - 1, c)
            if result == "BANG_EQUAL != null":
                pointer += 1
            print(result)
        elif c == "<":
            result = checkNeighbor(file_contents, pointer - 1, c)
            if result == "LESS_EQUAL <= null":
                pointer += 1
            print(result)
        elif c == ">":
            result = checkNeighbor(file_contents, pointer - 1, c)
            if result == "GREATER_EQUAL >= null":
                pointer += 1
            print(result)
        elif c == "/":
            result = checkNeighbor(file_contents, pointer - 1, c)
            if result == "EOF  null":
                while file_contents[pointer-1] not in ["\n", ""]:
                    pointer += 1
                    if pointer == len(file_contents):
                        break
            else:
                print(result)
        elif c == " " or c == "\t" or c == "\n":
            pass
        elif c == '"':
            #check if string
            checkString(pointer, file_contents, pointer)
        else:
            err = True
            error_message = f"[line {findlinenum(file_contents, c, pointer)}] " + f"Error: Unexpected character: {c}"
            print(error_message, file=sys.stderr)
    print("EOF  null")
    if err:
        sys.exit(65)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
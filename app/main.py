import sys

RESERVED_WORDS = {
    "and", "class", "else", "false", "for", "fun", 
    "if", "nil", "or", "print", "return", "super", 
    "this", "true", "var", "while"
}

def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <tokenize|parse|evaluate> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse", "evaluate"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
        
    if command == "tokenize":
        tokenize(file_contents)
    elif command == "parse":
        parse(file_contents)
    elif command == "evaluate":
        result = evaluate(file_contents)
        print(result)

def tokenize(file_contents):
    error = False
    i = 0
    line = 1

    while i < len(file_contents):
        c = file_contents[i]

        if c == "\n":
            line += 1
        elif c == "(":
            print("LEFT_PAREN ( null")
        elif c == "{":
            print("LEFT_BRACE { null")
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
        elif c == "}":
            print("RIGHT_BRACE } null")
        elif c == ")":
            print("RIGHT_PAREN ) null")
        elif c == "=":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("EQUAL_EQUAL == null")
                i += 1
            else:
                print("EQUAL = null")
        elif c == "!":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("BANG_EQUAL != null")
                i += 1
            else:
                print("BANG ! null")
        elif c == "<":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("LESS_EQUAL <= null")
                i += 1
            else:
                print("LESS < null")
        elif c == ">":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                print("GREATER_EQUAL >= null")
                i += 1
            else:
                print("GREATER > null")
        elif c == "/":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "/":
                i += 2
                while i < len(file_contents) and file_contents[i] != "\n":
                    i += 1
                line += 1
            else:
                print("SLASH / null")
        elif c in " \r\t":
            pass
        elif c == '"':
            word = ""
            i += 1
            while i < len(file_contents) and file_contents[i] != '"':
                word += file_contents[i]
                i += 1
            if i == len(file_contents):
                error = True
                print(f"[line {line}] Error: Unterminated string.", file=sys.stderr)
            else:
                print(f'STRING "{word}" {word}')
        elif c.isdigit():
            start = i
            has_dot = False
            while i < len(file_contents) and (file_contents[i].isdigit() or file_contents[i] == "."):
                if file_contents[i] == ".":
                    if has_dot:
                        error = True
                        print(f"[line {line}] Error: Unexpected character: .", file=sys.stderr)
                        break
                    has_dot = True
                i += 1
            number = file_contents[start:i]
            try:
                float_value = float(number)
                if float_value.is_integer():
                    normalized_value = f"{int(float_value)}.0"
                else:
                    normalized_value = f"{float_value:.2f}"
                print(f"NUMBER {number} {normalized_value}")
            except ValueError:
                error = True
                print(f"[line {line}] Error: Invalid number literal: {number}", file=sys.stderr)
            continue
        elif c.isalpha() or c == "_":
            start = i
            while i < len(file_contents) and (file_contents[i].isalnum() or file_contents[i] == "_"):
                i += 1
            identifier = file_contents[start:i]
            if identifier in RESERVED_WORDS:
                print(f"{identifier.upper()} {identifier} null")
            else:
                print(f"IDENTIFIER {identifier} null")
            continue
        else:
            error = True
            print(f"[line {line}] Error: Unexpected character: {c}", file=sys.stderr)
        i += 1

    print("EOF  null")
    if error:
        exit(65)
    else:
        exit(0)

def parse(file_contents):
    tokens = []
    i = 0
    line = 1
    error = False

    while i < len(file_contents):
        c = file_contents[i]

        if c == "\n":
            line += 1
        elif c in " \r\t":
            pass
        elif c.isdigit():
            start = i
            has_dot = False
            while i < len(file_contents) and (file_contents[i].isdigit() or file_contents[i] == "."):
                if file_contents[i] == ".":
                    if has_dot:
                        error = True
                        print(f"[line {line}] Error: Unexpected character: .", file=sys.stderr)
                        break
                    has_dot = True
                i += 1
            number = file_contents[start:i]
            try:
                float_value = float(number)
                if float_value.is_integer():
                    normalized_value = f"{int(float_value)}.0"
                else:
                    normalized_value = f"{float_value:.2f}".rstrip('0').rstrip('.')
                tokens.append(normalized_value)
            except ValueError:
                error = True
                print(f"[line {line}] Error: Invalid number literal: {number}", file=sys.stderr)
                break
            continue
        elif c == '"':
            word = ""
            i += 1
            while i < len(file_contents) and file_contents[i] != '"':
                word += file_contents[i]
                i += 1
            if i == len(file_contents):
                error = True
                print(f"[line {line}] Error: Unterminated string literal.", file=sys.stderr)
                break
            tokens.append(word)
        elif c == "+":
            tokens.append("+")
        elif c == "-":
            tokens.append("-")
        elif c == "*":
            tokens.append("*")
        elif c == "/":
            tokens.append("/")
        elif c == "(":
            tokens.append("(")
        elif c == ")":
            tokens.append(")")
        elif c == "!":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append("!=")
                i += 1
            else:
                tokens.append("!")
        elif c == "=":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append("==")
                i += 1
            else:
                tokens.append("=")
        elif c == "<":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append("<=")
                i += 1
            else:
                tokens.append("<")
        elif c == ">":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                tokens.append(">=")
                i += 1
            else:
                tokens.append(">")
        elif c.isalpha() or c == "_":
            start = i
            while i < len(file_contents) and (file_contents[i].isalnum() or file_contents[i] == "_"):
                i += 1
            identifier = file_contents[start:i]
            tokens.append(identifier)
            continue
        else:
            error = True
            print(f"[line {line}] Error: Unexpected character: {c}", file=sys.stderr)
            break
        i += 1

def evaluate(file_contents):
    tokens = []
    i = 0
    line = 1
    error = False

    while i < len(file_contents):
        c = file_contents[i]

        if c == "\n":
            line += 1
        elif c in " \r\t":
            pass
        elif c.isdigit():
            start = i
            has_dot = False
            while i < len(file_contents) and (file_contents[i].isdigit() or file_contents[i] == "."):
                if file_contents[i] == ".":
                    if has_dot:
                        print(f"[line {line}] Error: Unexpected character: .", file=sys.stderr)
                        sys.exit(65)
                    has_dot = True
                i += 1
            number = float(file_contents[start:i])
            tokens.append(number)
            continue
        elif file_contents.startswith("true", i):
            tokens.append(True)
            i += 4
        elif file_contents.startswith("false", i):
            tokens.append(False)
            i += 5
        elif file_contents.startswith("nil", i):
            tokens.append(None)
            i += 3
        elif c in "+-*/":
            tokens.append(c)
        else:
            error = True
            print(f"[line {line}] Error: Unexpected character: {c}", file=sys.stderr)
            sys.exit(65)
        i += 1

    print(f"Tokens: {tokens}", file=sys.stderr)
    if not error:
        ast = parse_expression(tokens, line)
        print(f"AST: {ast}", file=sys.stderr)
        if isinstance(ast, list): 
            result = evaluate_expression(ast)
            if result is not None:
                return result
            else:
                sys.exit(65)
        else:
            print("Error: Failed to parse a valid expression.", file=sys.stderr)
            sys.exit(65)
    else:
        sys.exit(65)

def evaluate_expression(tokens):
    if not isinstance(tokens, list):
        print(f"Error: Expected a list of tokens, but got {type(tokens).__name__}.", file=sys.stderr)
        sys.exit(65)
    
    if len(tokens) == 1:
        token = tokens[0]
        if token is True:
            return "true"
        elif token is False:
            return "false"
        elif token is None:
            return "nil"
        elif isinstance(token, (int, float)):
            return str(token)

    if len(tokens) == 3:
        left, operator, right = tokens
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if operator == "+":
                return str(left + right)
            elif operator == "-":
                return str(left - right)
            elif operator == "*":
                return str(left * right)
            elif operator == "/":
                return str(left / right)
        if operator == "==":
            return "true" if left == right else "false"
        elif operator == "!=":
            return "true" if left != right else "false"

    print("Error: Invalid expression or token structure.", file=sys.stderr)
    sys.exit(65)

def parse_expression(tokens, line):
    if len(tokens) == 0:
        print(f"[line {line}] Error: Expect expression.", file=sys.stderr)
        sys.exit(65)
    if tokens[0] in ("+", "*", "/"):
        print(f"[line {line}] Error: Operator '{tokens[0]}' without an operand.", file=sys.stderr)
        exit(65)
    expr = parse_equality(tokens, line)

    while len(tokens) > 0 and tokens[0] in ("+", "-"):
        operator = tokens.pop(0)
        if len(tokens) == 0 or tokens[0] in ("+", "-", "*", "/", "==", "!="):
            print(f"[line {line}] Error: Expect expression after '{operator}'.", file=sys.stderr)
            sys.exit(65)
        right = parse_equality(tokens, line)
        if right is None:
            print(f"[line {line}] Error: Expect expression after '{operator}'.", file=sys.stderr)
            sys.exit(65)
        expr = f"({operator} {expr} {right})"
    return expr

def parse_equality(tokens, line):
    left = parse_comparison(tokens, line)
    while len(tokens) > 0 and tokens[0] in ("==", "!="):
        operator = tokens.pop(0)
        if len(tokens) == 0 or tokens[0] in ("+", "-", "*", "/", "==", "!="):
            print(f"[line {line}] Error: Expect expression after '{operator}'.", file=sys.stderr)
            sys.exit(65)
        right = parse_comparison(tokens, line)
        left = f"({operator} {left} {right})"
    return left

def parse_comparison(tokens, line):
    left = parse_term(tokens, line)

    while len(tokens) > 0 and tokens[0] in ("<", ">", "<=", ">="):
        operator = tokens.pop(0)
        if len(tokens) == 0:
            report_error(operator, line, "Expect expression after operator.")
            exit(65)
            return None
        right = parse_term(tokens, line)
        left = f"({operator} {left} {right})"
    return left

def parse_term(tokens, line):
    left = parse_factor(tokens, line)

    while len(tokens) > 0 and tokens[0] in ("+", "-"):
        operator = tokens.pop(0)
        if len(tokens) == 0 or tokens[0] in ("+", "-", "*", "/", "==", "!="):
            print(f"[line {line}] Error: Expect expression after '{operator}'.", file=sys.stderr)
            sys.exit(65)
        right = parse_factor(tokens, line)
        left = f"({operator} {left} {right})"
    return left

def parse_factor(tokens, line):
    left = parse_unary(tokens, line)

    while len(tokens) > 0 and tokens[0] in ("*", "/"):
        operator = tokens.pop(0)
        if len(tokens) == 0:
            report_error(operator, line, "Expect expression after operator.")
            exit(65)
            return None
        right = parse_unary(tokens, line)
        left = f"({operator} {left} {right})"
    return left

def parse_unary(tokens, line):
    if len(tokens) == 0:
        return None

    token = tokens.pop(0)

    if token == "(":
        expr = parse_expression(tokens, line)
        if len(tokens) > 0 and tokens[0] == ")":
            tokens.pop(0)
            return f"(group {expr})"
        else:
            report_error(")", line, "Mismatched parentheses.")
            sys.exit(65)
    elif token == ")":
        report_error(")", line, "Unexpected ')' without matching '('.")
        return None
    elif token == "!":
        operand = parse_unary(tokens, line)
        return f"(! {operand})"
    elif token == "-":
        operand = parse_unary(tokens, line)
        return f"(- {operand})"
    return token

def report_error(token, line, message):
    print(f"[line {line}] Error at '{token}': {message}", file=sys.stderr)
    sys.exit(65)

if __name__ == "__main__":
    main()
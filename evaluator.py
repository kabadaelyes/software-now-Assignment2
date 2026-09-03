"""Recursive-descent arithmetic expression evaluator."""

from tokenizer import tokenize


def parse(tokens: list[tuple[str, str]]) -> tuple:
    """Parse a complete token list and return its expression tree."""
    tree, position = parse_expression(tokens, 0)

    if tokens[position][0] != "END":
        raise ValueError(f"Unexpected token {tokens[position]}")

    return tree


def parse_expression(tokens: list[tuple[str, str]], position: int) -> tuple:
    """Parse left-associative addition and subtraction."""
    left, position = parse_term(tokens, position)

    while tokens[position] in (("OP", "+"), ("OP", "-")):
        operator = tokens[position][1]
        right, position = parse_term(tokens, position + 1)
        left = (operator, left, right)

    return left, position


def parse_term(tokens: list[tuple[str, str]], position: int) -> tuple:
    """Parse multiplication, division, modulo, and implicit multiplication."""
    left, position = parse_unary(tokens, position)

    while True:
        token_type, value = tokens[position]

        if token_type == "OP" and value in ("*", "/", "%"):
            operator = value
            right, position = parse_unary(tokens, position + 1)
        elif token_type == "LPAREN":
            # Examples: 2(3 + 4) and (1 + 2)(3 + 4)
            operator = "*"
            right, position = parse_unary(tokens, position)
        elif token_type == "NUM" and tokens[position - 1][0] == "RPAREN":
            # Example: (1 + 2)3. Plain adjacent numbers such as 2 3 are invalid.
            operator = "*"
            right, position = parse_unary(tokens, position)
        else:
            break

        left = (operator, left, right)

    return left, position


def parse_unary(tokens: list[tuple[str, str]], position: int) -> tuple:
    """Parse prefix negation; unary plus is intentionally unsupported."""
    if tokens[position] == ("OP", "-"):
        operand, position = parse_unary(tokens, position + 1)
        return ("neg", operand), position

    if tokens[position] == ("OP", "+"):
        raise ValueError("Unary plus is not supported")

    return parse_power(tokens, position)


def parse_power(tokens: list[tuple[str, str]], position: int) -> tuple:
    """Parse right-associative exponentiation."""
    left, position = parse_primary(tokens, position)

    if tokens[position] == ("OP", "^"):
        right, position = parse_unary(tokens, position + 1)
        left = ("^", left, right)

    return left, position


def parse_primary(tokens: list[tuple[str, str]], position: int) -> tuple:
    """Parse a number or a parenthesised expression."""
    token_type, value = tokens[position]

    if token_type == "NUM":
        return ("num", value), position + 1

    if token_type == "LPAREN":
        tree, position = parse_expression(tokens, position + 1)

        if tokens[position][0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        return tree, position + 1

    raise ValueError(f"Expected a number or '(', found {tokens[position]}")


def parse_text(expression: str) -> tuple:
    """Tokenize and parse one expression."""
    return parse(tokenize(expression))


def format_tree(tree: tuple) -> str:
    """Convert an expression tree to the assignment's prefix format."""
    if tree[0] == "num":
        return tree[1]

    if tree[0] == "neg":
        return f"(neg {format_tree(tree[1])})"

    operator, left, right = tree
    return f"({operator} {format_tree(left)} {format_tree(right)})"


def evaluate_tree(tree: tuple) -> float:
    """Recursively calculate the numeric value of an expression tree."""
    node_type = tree[0]

    if node_type == "num":
        return float(tree[1])

    if node_type == "neg":
        return -evaluate_tree(tree[1])

    operator, left_tree, right_tree = tree
    left_value = evaluate_tree(left_tree)
    right_value = evaluate_tree(right_tree)

    if operator == "+":
        return left_value + right_value
    if operator == "-":
        return left_value - right_value
    if operator == "*":
        return left_value * right_value
    if operator == "/":
        return left_value / right_value
    if operator == "%":
        return left_value % right_value
    if operator == "^":
        result = left_value**right_value
        if isinstance(result, complex):
            raise ValueError("Complex results are not supported")
        return result

    raise ValueError(f"Unknown operator {operator!r}")


def evaluate_text(expression: str) -> float:
    """Tokenize, parse, and evaluate one expression."""
    return evaluate_tree(parse_text(expression))

def format_result(value: float) -> str:
    """Format a numeric result (rounding) as required in the assignment output."""
    if value.is_integer():
        return str(int(value))
    else:
        return str(round(value, 4))

def evaluate_file(input_file: str, output_file: str) -> None:
    """Read expressions from an input file, evaluate them, and write results to an output file."""
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            expression = line.strip()
            print(expression)

    return results

"""Recursive-descent arithmetic expression evaluator."""

import os

from tokenizer import tokenize, format_tokens


def parse(tokens):
    pos = 0

    def current():
        return tokens[pos]

    def consume(expected_type=None):
        nonlocal pos

        tok = current()

        if expected_type and tok[0] != expected_type:
            raise ValueError(
                f"Expected {expected_type} but got {tok[0]}"
            )

        pos += 1
        return tok

    def parse_primary():
        tok = current()

        if tok[0] == "NUM":
            return ("num", consume()[1])

        elif tok[0] == "LPAREN":
            consume()
            node = parse_expr()
            consume("RPAREN")
            return node

        raise ValueError(f"Unexpected token {tok}")

    def parse_power():
        node = parse_primary()

        if current()[0] == "OP" and current()[1] == "^":
            consume()

            # Parse the exponent as a unary expression so that
            # expressions such as 2^-3 are supported.
            right = parse_unary()

            node = ("^", node, right)

        return node

    def parse_unary():
        tok = current()

        if tok[0] == "OP" and tok[1] == "-":
            consume()

            # Prefix negation can be repeated, for example --5.
            return ("neg", parse_unary())

        elif tok[0] == "OP" and tok[1] == "+":
            # Unary + is intentionally unsupported.
            raise ValueError("Unary + is not supported")

        return parse_power()

    def parse_term():
        node = parse_unary()

        while True:
            tok = current()

            if tok[0] == "OP" and tok[1] in ("*", "/", "%"):
                op = consume()[1]
                node = (op, node, parse_unary())

            elif tok[0] == "LPAREN":
                # Examples: 2(3 + 4) and (1 + 2)(3 + 4)
                node = ("*", node, parse_unary())

            elif (
                tok[0] == "NUM"
                and pos > 0
                and tokens[pos - 1][0] == "RPAREN"
            ):
                # Example: (1 + 2)3.
                # Plain adjacent numbers such as 2 3 are invalid.
                node = ("*", node, parse_unary())

            else:
                break

        return node

    def parse_expr():
        node = parse_term()

        while current()[0] == "OP" and current()[1] in ("+", "-"):
            op = consume()[1]
            node = (op, node, parse_term())

        return node

    ast = parse_expr()

    if current()[0] != "END":
        raise ValueError("Trailing tokens found")

    return ast


def format_tree(node):
    """Convert an expression tree to the assignment's prefix format."""
    if node[0] == "num":
        return node[1]

    if node[0] == "neg":
        return f"(neg {format_tree(node[1])})"

    return (
        f"({node[0]} "
        f"{format_tree(node[1])} "
        f"{format_tree(node[2])})"
    )


def evaluate_ast(node):
    """Recursively calculate the numeric value of an expression tree."""
    if node[0] == "num":
        return float(node[1])

    if node[0] == "neg":
        return -evaluate_ast(node[1])

    op = node[0]

    left = evaluate_ast(node[1])
    right = evaluate_ast(node[2])

    if op == "+":
        return left + right

    if op == "-":
        return left - right

    if op == "*":
        return left * right

    if op == "/":
        if right == 0:
            raise ZeroDivisionError()

        return left / right

    if op == "%":
        if right == 0:
            raise ZeroDivisionError()

        return left % right

    if op == "^":
        result = left ** right

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported")

        return result

    raise ValueError(f"Unknown operator {op!r}")


def evaluate_text(expression: str) -> float:
    """Tokenize, parse, and evaluate one expression."""
    tokens = tokenize(expression)
    return evaluate_ast(parse(tokens))


def format_result(value: float) -> str:
    """Format a numeric result (rounding) as required in the assignment output."""
    if value.is_integer():
        return str(int(value))

    return str(round(value, 4))


def evaluate_file(input_path: str) -> list[dict]:
    """Read expressions from an input file, evaluate them, and write results to an output file."""
    results = []
    output_lines = []

    with open(input_path, "r") as infile:
        lines = infile.readlines()

    for raw_line in lines:
        expression = raw_line.rstrip("\r\n")

        if not expression.strip():
            continue

        entry = {
            "input": expression,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

        try:
            tokens = tokenize(expression)

            # Plain adjacent numbers such as 2 3 are invalid.
            # Implicit multiplication is only allowed after a closing
            # parenthesis, or before a parenthesis.
            for i in range(len(tokens) - 1):
                if (
                    tokens[i][0] == "NUM"
                    and tokens[i + 1][0] == "NUM"
                ):
                    raise ValueError(
                        "Adjacent numbers are not allowed"
                    )

            entry["tokens"] = format_tokens(tokens)

            ast = parse(tokens)

            entry["tree"] = format_tree(ast)

            result = evaluate_ast(ast)

            entry["result"] = float(result)

        except Exception:
            pass

        results.append(entry)

        output_lines.append(
            f"Input: {entry['input']}"
        )

        output_lines.append(
            f"Tree: {entry['tree']}"
        )

        output_lines.append(
            f"Tokens: {entry['tokens']}"
        )

        if entry["result"] == "ERROR":
            output_result = "ERROR"
        else:
            output_result = format_result(entry["result"])

        output_lines.append(
            f"Result: {output_result}"
        )

        output_lines.append("")

    # Create output.txt in the same directory as input_path
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(input_path)),
        "output.txt"
    )

    with open(output_path, "w") as outfile:
        outfile.write("\n".join(output_lines))

    return results


if __name__ == "__main__":
    results = evaluate_file("sample_input.txt")
    print(
        f"Successfully processed {len(results)} expressions. "
        "Check output.txt!"
    )
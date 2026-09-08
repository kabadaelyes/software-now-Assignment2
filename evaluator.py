from tokenizer import tokenize, format_tokens


def parse(tokens):
    position = 0

    def current():
        return tokens[position]

    def consume(expected_type=None):
        nonlocal position

        token = current()

        if expected_type is not None and token[0] != expected_type:
            raise ValueError(
                f"Expected {expected_type} but got {token[0]}"
            )

        position += 1
        return token

    def parse_primary():
        token = current()

        if token[0] == "NUM":
            return ("num", consume()[1])

        if token[0] == "LPAREN":
            consume("LPAREN")
            node = parse_expression()
            consume("RPAREN")
            return node

        raise ValueError(f"Unexpected token {token}")

    def parse_power():
        left = parse_primary()

        if current() == ("OP", "^"):
            consume("OP")
            right = parse_unary()
            return ("^", left, right)

        return left

    def parse_unary():
        token = current()

        if token == ("OP", "-"):
            consume("OP")
            return ("neg", parse_unary())

        if token == ("OP", "+"):
            raise ValueError("Unary + is not supported")

        return parse_power()

    def parse_term():
        node = parse_unary()

        while True:
            token_type, value = current()

            if token_type == "OP" and value in ("*", "/", "%"):
                operator = consume()[1]
                right = parse_unary()
                node = (operator, node, right)

            elif token_type == "LPAREN":
                # Example: 2(3 + 4)
                right = parse_unary()
                node = ("*", node, right)

            else:
                break

        return node

    def parse_expression():
        node = parse_term()

        while current()[0] == "OP" and current()[1] in ("+", "-"):
            operator = consume()[1]
            right = parse_term()
            node = (operator, node, right)

        return node

    tree = parse_expression()

    if current()[0] != "END":
        raise ValueError(f"Unexpected token {current()}")

    return tree


def format_tree(tree):
    if tree[0] == "num":
        return tree[1]

    if tree[0] == "neg":
        return f"(neg {format_tree(tree[1])})"

    operator, left, right = tree

    return f"({operator} {format_tree(left)} {format_tree(right)})"


def evaluate_tree(tree):
    node_type = tree[0]

    if node_type == "num":
        return float(tree[1])

    if node_type == "neg":
        return -evaluate_tree(tree[1])

    operator, left_tree, right_tree = tree

    left = evaluate_tree(left_tree)
    right = evaluate_tree(right_tree)

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        return left / right

    if operator == "%":
        if right == 0:
            raise ZeroDivisionError("Modulo by zero")
        return left % right

    if operator == "^":
        result = left ** right

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported")

        return result

    raise ValueError(f"Unknown operator: {operator}")


def evaluate_text(expression):
    tokens = tokenize(expression)
    tree = parse(tokens)
    return evaluate_tree(tree)


def format_result(value):
    if float(value).is_integer():
        return str(int(value))

    return str(round(value, 4))


def evaluate_file(input_path):
    results = []
    output_lines = []

    with open(input_path, "r") as file:
        lines = file.readlines()

    for raw_line in lines:

        expression = raw_line.rstrip("\n")

        # Skip completely empty lines
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

            # Reject adjacent numbers such as "2 3"
            for i in range(len(tokens) - 1):
                current_token = tokens[i]
                next_token = tokens[i + 1]

                if (
                    current_token[0] == "NUM"
                    and next_token[0] == "NUM"
                ):
                    raise ValueError("Adjacent numbers are not allowed")

            entry["tokens"] = format_tokens(tokens)

            tree = parse(tokens)
            entry["tree"] = format_tree(tree)

            result = evaluate_tree(tree)

            entry["result"] = float(result)

        except Exception:
            pass

        results.append(entry)

        output_lines.append(f"Input: {entry['input']}")
        output_lines.append(f"Tree: {entry['tree']}")
        output_lines.append(f"Tokens: {entry['tokens']}")

        if entry["result"] == "ERROR":
            output_result = "ERROR"
        else:
            output_result = format_result(entry["result"])

        output_lines.append(f"Result: {output_result}")
        output_lines.append("")

    # Create output.txt in the same directory as input_path
    import os

    output_path = os.path.join(
        os.path.dirname(input_path),
        "output.txt"
    )

    with open(output_path, "w") as file:
        file.write("\n".join(output_lines))

    return results


if __name__ == "__main__":
    results = evaluate_file("sample_input.txt")

    print(
        f"Successfully processed {len(results)} expressions. "
        f"Check output.txt!"
    )
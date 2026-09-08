# Operators used in the expressions
OPERATORS = "+-*/%^"


def tokenize(expression: str) -> list[tuple[str, str]]:
    """Split the expression into tokens."""
    tokens = []
    position = 0

    while position < len(expression):
        character = expression[position]

        # Ignore spaces
        if character.isspace():
            position += 1
            continue

        # Read numbers
        if "0" <= character <= "9":
            start = position

            while (
                position < len(expression)
                and "0" <= expression[position] <= "9"
            ):
                position += 1

            # Check for decimal numbers
            if position < len(expression) and expression[position] == ".":
                position += 1

                if not (
                    position < len(expression)
                    and "0" <= expression[position] <= "9"
                ):
                    raise ValueError(
                        f"Malformed number at position {start}"
                    )

                while (
                    position < len(expression)
                    and "0" <= expression[position] <= "9"
                ):
                    position += 1

            tokens.append(("NUM", expression[start:position]))
            continue

        # Operators
        if character in OPERATORS:
            tokens.append(("OP", character))

        # Opening bracket
        elif character == "(":
            tokens.append(("LPAREN", character))

        # Closing bracket
        elif character == ")":
            tokens.append(("RPAREN", character))

        # Anything else is invalid
        else:
            raise ValueError(
                f"Unexpected character {character!r} at position {position}"
            )

        position += 1

    # Mark the end of the expression
    tokens.append(("END", ""))

    return tokens


def format_tokens(tokens: list[tuple[str, str]]) -> str:
    """Format tokens for output.txt."""
    formatted = []

    for token_type, value in tokens:

        if token_type == "END":
            formatted.append("[END]")
        else:
            formatted.append(f"[{token_type}:{value}]")

    return " ".join(formatted)
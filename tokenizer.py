"""Tokenization helpers for the arithmetic expression evaluator.

Tokens are represented as ``(type, value)`` tuples so the assignment remains
function-based and does not require token classes.
"""


OPERATORS = "+-*/%^"


def tokenize(expression: str) -> list[tuple[str, str]]:
    """Convert an expression string into a list of tokens.

    Whitespace is ignored. A ``ValueError`` is raised for an unknown character
    or a malformed number. The returned list always ends with an END token.
    """
    tokens = []
    position = 0

    while position < len(expression):
        character = expression[position]

        if character.isspace():
            position += 1
            continue

        if "0" <= character <= "9":
            start = position

            while (
                position < len(expression)
                and "0" <= expression[position] <= "9"
            ):
                position += 1

            if position < len(expression) and expression[position] == ".":
                position += 1

                #  requires one or more digits after the decimal point.
                if not (
                    position < len(expression)
                    and "0" <= expression[position] <= "9"
                ):
                    raise ValueError(f"Malformed number at position {start}")

                while (
                    position < len(expression)
                    and "0" <= expression[position] <= "9"
                ):
                    position += 1

            tokens.append(("NUM", expression[start:position]))
            continue

        if character in OPERATORS:
            tokens.append(("OP", character))
        elif character == "(":
            tokens.append(("LPAREN", character))
        elif character == ")":
            tokens.append(("RPAREN", character))
        else:
            raise ValueError(
                f"Unexpected character {character!r} at position {position}"
            )

        position += 1

    tokens.append(("END", ""))
    return tokens


def format_tokens(tokens: list[tuple[str, str]]) -> str:
    """Format tokens exactly as required in the assignment output."""
    formatted = []

    for token_type, value in tokens:
        if token_type == "END":
            formatted.append("[END]")
        else:
            formatted.append(f"[{token_type}:{value}]")

    return " ".join(formatted)

def tokenize(expression):
    tokens = []
    token_strs = []
    pos = 0
    while pos < len(expression):
        char = expression[pos]
        if char.isspace():
            pos += 1
            continue
        
        if char in "+-*/%^":
            tokens.append(('OP', char))
            token_strs.append(f"[OP:{char}]")
            pos += 1
        elif char == '(':
            tokens.append(('LPAREN', '('))
            token_strs.append("[LPAREN:(]")
            pos += 1
        elif char == ')':
            tokens.append(('RPAREN', ')'))
            token_strs.append("[RPAREN:)]")
            pos += 1
        elif char.isdigit():
            start_pos = pos
            while pos < len(expression) and expression[pos].isdigit():
                pos += 1
            if pos < len(expression) and expression[pos] == '.':
                if pos + 1 < len(expression) and expression[pos+1].isdigit():
                    pos += 1
                    while pos < len(expression) and expression[pos].isdigit():
                        pos += 1
            
            val = expression[start_pos:pos]
            float_val = float(val)
            tokens.append(('NUM', float_val))
            display_val = str(int(float_val)) if float_val.is_integer() else val
            token_strs.append(f"[NUM:{display_val}]")
        else:
            raise ValueError(f"Invalid character: {char}")
            
    tokens.append(('END', ''))
    token_strs.append("[END]")
    return tokens, " ".join(token_strs)

def parse(tokens):
    pos = 0

    def current():
        return tokens[pos] if pos < len(tokens) else ('END', '')

    def consume(expected_type=None):
        nonlocal pos
        tok = current()
        if expected_type and tok[0] != expected_type:
            raise ValueError(f"Expected {expected_type} but got {tok[0]}")
        pos += 1
        return tok

    def parse_primary():
        tok = current()
        if tok[0] == 'NUM':
            return consume()[1]
        elif tok[0] == 'LPAREN':
            consume()
            node = parse_expr()
            consume('RPAREN')
            return node
        raise ValueError(f"Unexpected token {tok}")

    def parse_power():
        node = parse_primary()
        if current()[0] == 'OP' and current()[1] == '^':
            consume()
            right = parse_power() 
            node = ('^', node, right)
        return node

    def parse_unary():
        tok = current()
        if tok[0] == 'OP' and tok[1] == '-':
            consume()
            return ('neg', parse_unary())
        elif tok[0] == 'OP' and tok[1] == '+':
            raise ValueError("Unary + is not supported")
        return parse_power()

    def parse_term():
        node = parse_unary()
        while True:
            tok = current()
            if tok[0] == 'OP' and tok[1] in ('*', '/', '%'):
                op = consume()[1]
                node = (op, node, parse_unary())
            elif tok[0] in ('NUM', 'LPAREN'):
                node = ('*', node, parse_unary())
            else:
                break
        return node

    def parse_expr():
        node = parse_term()
        while current()[0] == 'OP' and current()[1] in ('+', '-'):
            op = consume()[1]
            node = (op, node, parse_term())
        return node

    ast = parse_expr()
    if current()[0] != 'END':
        raise ValueError("Trailing tokens found")
    return ast

def format_tree(node):
    if isinstance(node, tuple):
        if node[0] == 'neg':
            return f"(neg {format_tree(node[1])})"
        return f"({node[0]} {format_tree(node[1])} {format_tree(node[2])})"
    return str(int(node)) if float(node).is_integer() else str(node)

def evaluate_ast(node):
    if isinstance(node, tuple):
        op = node[0]
        if op == 'neg':
            return -evaluate_ast(node[1])
            
        left = evaluate_ast(node[1])
        right = evaluate_ast(node[2])
        
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/':
            if right == 0: raise ZeroDivisionError()
            return left / right
        if op == '%':
            if right == 0: raise ZeroDivisionError()
            return left % right
        if op == '^': return left ** right
    return node

def evaluate_file(input_path: str) -> list[dict]:
    results = []
    output_lines = []
    
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        entry = {
            "input": line,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

        try:
            tokens, token_str = tokenize(line)
            entry["tokens"] = token_str
            
            ast = parse(tokens)
            entry["tree"] = format_tree(ast)
            
            res = evaluate_ast(ast)
            if isinstance(res, (int, float)):
                if float(res).is_integer():
                    entry["result"] = int(res)
                else:
                    entry["result"] = round(res, 4)
        except Exception:
            pass 

        results.append(entry)
        
        output_lines.append(f"Input: {entry['input']}")
        output_lines.append(f"Tree: {entry['tree']}")
        output_lines.append(f"Tokens: {entry['tokens']}")
        output_lines.append(f"Result: {entry['result']}\n")

    if '/' in input_path:
        out_path = input_path.rsplit('/', 1)[0] + '/output.txt'
    elif '\\' in input_path:
        out_path = input_path.rsplit('\\', 1)[0] + '\\output.txt'
    else:
        out_path = 'output.txt'

    with open(out_path, 'w') as f:
        f.write("\n".join(output_lines).strip() + "\n")
        
    return results

if __name__ == "__main__":
    results = evaluate_file("sample_input.txt")
    print(f"Successfully processed {len(results)} expressions. Check output.txt!")
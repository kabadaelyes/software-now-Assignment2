# software-now-Assignment2

# Overview
This is a group-based python project containing two programs

1. Text-based encryption and decryption
2. Arithmetic expression evaluator using tokenisation


'cipher.py' - handles encryption and decryption.
'tokenizer.py' — processes and separates input text into tokens.
'evaluator.py' — evaluates the processed text and produces results.

## Question 1 - Cipher

`cipher.py` reads text from `raw_text.txt`, encrypts it using two user-provided shift values, decrypts the encrypted text, and verifies that the decrypted file matches the original.

Main files:
- `cipher.py`
- `raw_text.txt`
- `encrypted_text.txt`
- `decrypted_text.txt`

## Question 2 - Arithmetic Expression Evaluator

The program reads mathematical expressions from `input.txt`, tokenises and evaluates each expression using recursive descent parsing, and writes the results to `output.txt`.

Main files:
- `tokenizer.py` - converts expressions into tokens.
- `evaluator.py` - parses and evaluates the tokenised expressions.
- `input.txt` - contains the expressions to be evaluated.
- `output.txt` - contains the generated results.

Supported features:
- `+`, `-`, `*`, `/`, `%`
- exponentiation `^`
- parentheses
- unary negation
- implicit multiplication

Each result includes:
- Input
- Parse Tree
- Tokens
- Result







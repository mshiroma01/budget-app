import re

def tokenize(expression):
    tokens = re.findall(r'&&|\|\||<=|>=|!=|==|<|>|[\w/]+', expression)
    return tokens
    
def infix_to_postfix(tokens):
    precedence = {'||': 1, '&&': 2, '==': 3, '!=': 3, '>': 3, '<': 3, '>=': 3, '<=': 3}
    output = []
    operator_stack = []
    for token in tokens:
        if token in precedence:
            while operator_stack and precedence.get(operator_stack[-1], 0) >= precedence[token]:
                output.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Discard '('
        else:
            output.append(token)
    while operator_stack:
        output.append(operator_stack.pop())
    return output

def convert_to_postfix(expression):
    tokens = tokenize(expression)
    postfix_tokens = infix_to_postfix(tokens)
    return postfix_tokens

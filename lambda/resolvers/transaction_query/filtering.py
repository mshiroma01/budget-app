import datetime
import re
from parse_input import parse_input

def apply_filters(transactions, input_data):
    # Custom filtering logic based on input data
    filtered_transactions = []
    for transaction in transactions:
        matches_criteria = evaluate_conditions(transaction, input_data)
        if matches_criteria:
            filtered_transactions.append(transaction)

    return filtered_transactions

def tokenize(expression):
    tokens = re.findall(r'&&|\|\||\([^\s]+?\)|[^\s()]+', expression)
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

def evaluate_conditions(transaction, input_data):
    for field, condition in input_data.items():
        postfix_tokens = infix_to_postfix(tokenize(condition))
        if not evaluate_postfix(transaction.get(field), postfix_tokens, field):
            return False
    return True

def evaluate_postfix(field_value, postfix_tokens, field):
    operand_stack = []
    for token in postfix_tokens:
        if token == '&&':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 and operand2
            operand_stack.append(result)
        elif token == '||':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 or operand2
            operand_stack.append(result)
        else:
            data = parse_input(token)
            operator = data['operator']
            value = data['value']
            
            # It's an operand (field value)
            parsed_input = parse_input(token)
            operator = parsed_input['operator']
            value = parsed_input['value']
            
            # Need to change the value to the correct type
            if field in ['amount', 'balance']:
                value = float(value)
            elif field in ['transaction_date', 'post_date']:
                try:
                    value = datetime.datetime.strptime(value, '%m/%d/%Y').date()
                except ValueError:
                    pass
            
            if operator == '==':
                result = field_value == value
            elif operator == '!=':
                result = field_value != value
            elif operator == '<':
                result = field_value < value
            elif operator == '<=':
                result = field_value <= value
            elif operator == '>':
                result = field_value > value
            elif operator == '>=':
                result = field_value >= value
            operand_stack.append(result)
    return operand_stack.pop()
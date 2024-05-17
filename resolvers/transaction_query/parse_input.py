import re

def parse_input(input_string):
    # Define a regular expression pattern to match comparison operators
    operator_pattern = r'(<=|<|>=|>|!=|==)'

    # Use regex to split the input into operator and value parts
    match = re.match(operator_pattern, input_string)
    if match:
        operator = match.group()
        field_value = input_string.split(operator, 1)[-1].strip()  # Get the value after the operator
        return {'operator': operator, 'value': field_value}
    else:
        # If no operator is found, assume equality comparison
        return {'operator': '==', 'value': input_string.strip()}

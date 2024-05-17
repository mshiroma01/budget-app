from dynamodb_utils import get_transactions_from_dynamodb
from filtering import apply_filters

def lambda_handler(event, context):
    # Extract filter input from the GraphQL event
    input_data = event.get('arguments', {}).get('input', {})

    # Get transactions from DynamoDB based on the filter
    transactions = get_transactions_from_dynamodb()
    
    # Apply filters
    filtered_transactions = apply_filters(transactions, input_data)

    return filtered_transactions
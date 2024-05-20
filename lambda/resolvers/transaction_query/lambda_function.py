from dynamodb_utils import get_transactions_from_dynamodb
from filtering import apply_filters

def lambda_handler(event, context):
    # Extract filter input from the GraphQL event
    input_data = event.get('arguments', {}).get('input', {})

    # Get transactions from DynamoDB based on the filter
    transactions = get_transactions_from_dynamodb()
    
    # Apply filters
    filtered_transactions = apply_filters(transactions, input_data)
    # Convert transaction_date and post_date to string
    filtered_transactions = [
        {
            **transaction,
            'transaction_date': str(transaction['transaction_date']),
            'post_date': str(transaction['post_date'])
        }
        for transaction in filtered_transactions
    ]
    return filtered_transactions
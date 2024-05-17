import boto3

# Define the DynamoDB table name as a constant
TABLE_NAME = 'TransactionTable'

def get_transactions_from_dynamodb():
    # Create a DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # Get the DynamoDB table using the constant table name
    table = dynamodb.Table(TABLE_NAME)

    # Perform a scan operation to retrieve all items in the table
    response = table.scan()

    # Extract the items from the response
    items = response.get('Items', [])

    # Transform the items into the format expected by the application
    transactions = []
    for item in items:
        transaction = {
            'transaction_date': item.get('transaction_date', ''),
            'description': item.get('description', ''),
            'address': item.get('address', ''),
            'amount': float(item.get('amount', 0)),
            'balance': float(item.get('balance', 0)),
            'category': item.get('category', ''),
            'mapping_config_name': item.get('mapping_config_name', ''),
            'memo': item.get('memo', ''),
            'post_date': item.get('post_date', ''),
            'transaction_type': item.get('transaction_type', '')
        }
        transactions.append(transaction)

    return transactions
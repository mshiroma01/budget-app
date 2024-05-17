import boto3
from decimal import Decimal
import hashlib

DYNAMODB_TABLE_NAME = 'TransactionTable'

def lambda_handler(event, context):
    # Extract input data from the GraphQL event
    input_data = event.get('arguments', {}).get('input', {})
    
    # Convert float values to Decimal types
    for key, value in input_data.items():
        if isinstance(value, float):
            input_data[key] = Decimal(str(value))
    
    # Prepare the item to be added to DynamoDB
    item = {}
    for key in input_data:
        item[key] = input_data[key]
    item_string = ''.join(str(item.get(field, '')) for field in sorted(item.keys()))
    item['hash'] = hashlib.sha256(item_string.encode()).hexdigest()[:16]
    
    # Add the item to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.put_item(Item=item)
    
    # Return the response
    return item

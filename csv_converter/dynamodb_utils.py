from datetime import datetime
import boto3
from decimal import Decimal
import hashlib

TABLE_NAME = 'TransactionTable'

def update_dynamodb_from_csv(df, mapping_config, file_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    for _, row in df.iterrows():
        item = {}
        
        # Userid is the last part of the file name
        file_parts = file_name.split('/')[-1].split('_')
        user_id = file_parts[0]
        item['userid'] = user_id

        for key, value in mapping_config.items():
            if value in df.columns and key != 'name':
                if key == 'debit' and row[value] != "0":
                    debit_value = str(row['Debit']).replace('$', '').replace(',', '')
                    item['amount'] = Decimal(debit_value).quantize(Decimal('0.01')) * Decimal('-1')
                elif key == 'credit' and row[value] != "0":
                    credit_value = str(row['Credit']).replace('$', '').replace(',', '')
                    item['amount'] = Decimal(credit_value).quantize(Decimal('0.01'))
                elif key == 'payee':
                    item['description'] = str(row[value])
                elif key not in ['name', 'debit', 'credit', 'reference_number', 'payee']:
                    item[key] = str(row[value]) if row[value] is not None else None

        item['mapping_config_name'] = mapping_config['name']

        if 'amount' in item:
            item['amount'] = Decimal(str(item['amount']).replace(',', '')).quantize(Decimal('0.01'))
            
        if 'balance' in item:
            balance_value = str(item['balance']).replace('$', '').replace(',', '')
            item['balance'] = Decimal(balance_value).quantize(Decimal('0.01'))

        item_string = ''.join(str(item.get(field, '')) for field in sorted(item.keys()))
        item['hash'] = hashlib.sha256(item_string.encode()).hexdigest()[:16]
        
        response = table.put_item(Item=item)
        print(response)

    print(f'Successfully updated DynamoDB table with data from CSV with mapping: {mapping_config}')

def store_checksum_in_dynamodb(table_name, checksum, file_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Get the current datetime
    current_datetime = datetime.now().isoformat()
    
    file_parts = file_name.split('/')[-1].split('_')
    user_id = file_parts[0]

    # Put the item in the DynamoDB table
    table.put_item(Item={
        'checksum': checksum,
        'date_added': current_datetime,
        'user_id': user_id
    })

    print(f"Checksum '{checksum}' stored in DynamoDB table '{table_name}' with date '{current_datetime}'.")
    
def check_duplicate_checksum(table_name, checksum):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        response = table.get_item(
            Key={
                'checksum': checksum
            }
        )
        return 'Item' in response
    except Exception as e:
        print(f"An error occurred while checking for duplicate checksum: {e}")
        return False
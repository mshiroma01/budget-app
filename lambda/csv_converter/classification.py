import boto3

def get_classification_data(table_name, user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression='userid = :userid',
        ExpressionAttributeValues={
            ':userid': user_id  
        }
    )
    return response['Items']


def classification(item, table_data):
    if 'category' in item:
        for row in table_data:
            if row['userid'] == item['userid'] and row['category'] == item['category']:
                item['need'] = row['need']
                item['want'] = row['want']
                item['saving'] = row['saving']
                break
        else:
            # Dont store the other values in the item to save space in table
            item['need'] = -1
    else:
        # Dont store the other values in the item to save space in table
        item['need'] = -2
    
    return item

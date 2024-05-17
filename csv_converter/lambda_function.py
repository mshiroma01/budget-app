import boto3
import pandas as pd
import io
import hashlib
from dynamodb_utils import store_checksum_in_dynamodb, check_duplicate_checksum, update_dynamodb_from_csv
from utils import rename_file, get_csv_file_from_s3
from mapping_configurations import mapping_configs

# DynamoDB table name
CHECKSUMS_TABLE_NAME = 'ChecksumsTable'

def calculate_checksum(data):
    # Calculate MD5 checksum
    checksum = hashlib.md5(data).hexdigest()
    return checksum

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        file_content = get_csv_file_from_s3(s3, bucket, key)

        # Calculate checksum
        checksum = calculate_checksum(file_content)

        # Check if checksum already exists in DynamoDB
        if not check_duplicate_checksum(CHECKSUMS_TABLE_NAME, checksum):
            df_headers = pd.read_csv(io.BytesIO(file_content), nrows=1)
            header = df_headers.columns.tolist()
            
            if header == ['Description', 'Unnamed: 1', 'Summary Amt.']:
                header = ['Date', 'Description', 'Amount', 'Running Bal.']
                df = pd.read_csv(io.BytesIO(file_content), skiprows=8, header=None, names=header)
            else:
                df = pd.read_csv(io.BytesIO(file_content))
            
            mapping_config = None
            for format_name, config in mapping_configs.items():
                if all(col in header for key, col in config.items() if key != 'name'):
                    mapping_config = config
                    break
                    
            if mapping_config is not None:
                update_dynamodb_from_csv(df, mapping_config, key)
                new_key = rename_file(key, mapping_config, checksum)
                s3.copy_object(Bucket=bucket, Key=f'old-csvs/{new_key}', CopySource=f'{bucket}/{key}')
                s3.delete_object(Bucket=bucket, Key=key)
            else:
                print(f'No matching mapping configuration found for CSV file: {key}')

            # Store the checksum and date in DynamoDB
            store_checksum_in_dynamodb(CHECKSUMS_TABLE_NAME, checksum, key)
        else:
            print(f"File with checksum '{checksum}' has already been processed. Skipping further processing.")
            s3.delete_object(Bucket=bucket, Key=key)
            
    return {
        'statusCode': 200,
        'body': 'Successfully processed the S3 event'
    }
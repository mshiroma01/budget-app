from datetime import datetime

def get_csv_file_from_s3(s3, bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()

def rename_file(key, mapping_config, checksum):
    date_uploaded = datetime.now().strftime('%m-%d-%Y')
    new_file_name = f"{mapping_config['name']}-{date_uploaded}-{checksum}.csv"
    return new_file_name
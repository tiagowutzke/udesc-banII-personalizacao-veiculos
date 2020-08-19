import os
import boto3


def send_file_to_s3(filename, bucket, folder='images'):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    s3_file = f"blip-multimedia/{folder}/{filename}"

    s3_params = {
        'ACL': 'public-read'
    }

    try:
        s3.upload_file(filename, bucket, s3_file, ExtraArgs=s3_params)
        print("Upload Successful")
        return True
    except Exception as e:
        print(f"Error on send file to s3: {e}")
        return False


def delete_file_from_s3(file):
    bucket = os.environ.get('S3_BUCKET')
    s3 = boto3.resource("s3")

    aws_prefix = f"https://{bucket}.s3-sa-east-1.amazonaws.com/"
    key = file.replace(aws_prefix, '')

    try:
        obj = s3.Object(bucket, key)
        obj.delete()
    except Exception as e:
        print(f"Error on delete file to s3: {e}")
        return False


def get_file_from_s3(bucket, key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    response = s3.get_object(Bucket=bucket, Key=key)

    return response['Body'].read()


def get_s3_conn():
    return boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )


def list_files_from_s3(bucket, folder):
    s3 = get_s3_conn()
    return s3.list_objects_v2(Bucket=bucket, Prefix=folder)
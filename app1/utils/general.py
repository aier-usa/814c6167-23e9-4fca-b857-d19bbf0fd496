import os
from botocore.client import Config
import boto3


def s3_put_object(name, content, content_type):
    print("Filename inside s3_put_object is: ")
    print(name)
    # other choices for signature_version: s3v4, v4, AWS4-HMAC-SHA256,
    # inside environment variable now
    s3_signature_version = os.environ['AWS_S3_SIGNATURE_VERSION']
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        config=Config(
            signature_version=s3_signature_version)
    )
    bucket_name = os.environ['AWS_S3_BUCKET_NAME']
    s3.Bucket(bucket_name).put_object(
        ContentType=content_type,
        ACL='public-read',
        Key=name,
        Body=content)


def s3_delete_object(name):
    print("Filename inside s3_delete_object is: ")
    print(name)
    # other choices for signature_version: s3v4, v4, AWS4-HMAC-SHA256,
    # inside environment variable now
    s3_signature_version = os.environ['AWS_S3_SIGNATURE_VERSION']
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        config=Config(
            signature_version=s3_signature_version)
    )
    bucket_name = os.environ['AWS_S3_BUCKET_NAME']

    s3.Bucket(bucket_name).delete_objects(
        Delete={
            'Objects':
                [
                    {
                        'Key': name
                    },
                ],
            'Quiet': True
        }
    )
    print("Finished s3_delete_object")

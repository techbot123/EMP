import logging
import boto3
from botocore.exceptions import ClientError
# from . import secrets
from werkzeug.utils import secure_filename
from emdb.secrets import Access_key_ID, Access_secret_key
import random
import string
import io
from io import BytesIO
from PIL import Image

used_files = set()
DEFAULT_PATH_TO_S3 = 'employee/profile_img/'
DEFAULT_IMG_BUCKET_S3 = 'test-bucket-987123'
NO_IMG_S3 = 'employee/no_profile/image.jpeg'
DEFAULT_PAYSLIP_S3 = 'employee/pay_slips/'

def generate_filename(num = 10):
    global used_files
    for _ in range(5):
        _filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=num))
        if _filename in used_files:
            continue
        else:
            used_files.update(_filename)
            return _filename

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.resource('s3', aws_access_key_id = Access_key_ID,
                                        aws_secret_access_key = Access_secret_key)
            s3_client.create_bucket(Bucket=bucket_name,
                                    ACL='private')
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_file(file,
                bucket = DEFAULT_IMG_BUCKET_S3,
                object_name=DEFAULT_PATH_TO_S3):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    filename = generate_filename()
    file.filename = filename + '.' + file.filename.split('.')[-1]
    clients3 = boto3.resource('s3', aws_access_key_id = Access_key_ID,
                            aws_secret_access_key = Access_secret_key)
    my_bucket = clients3.Bucket(bucket)
    try:
        my_bucket.put_object(Key=object_name+file.filename, Body=file)
    except ClientError as e:
        logging.error(e)
        return (None, None)
    return (object_name+file.filename, bucket)

# def get_profile_image_s3(img_path_s3 = 'employee/no_profile/image.jpeg',
#                          bucket_name = 'test-bucket-987123'):
#
#     clients3 = boto3.resource('s3', aws_access_key_id = Access_key_ID,
#                             aws_secret_access_key = Access_secret_key)
#
#     # if profile_image:
#     my_bucket = clients3.Bucket(bucket_name)
#
#     obj_s3 = my_bucket.Object(img_path_s3).get()
#     #Extract body
#     body = obj_s3.get('Body')
#     #Open image with Image and BytesIO
#     scr = Image.open(BytesIO(body.read()))
#     return scr

def get_profile_image(img_path_s3 = NO_IMG_S3,
                      bucket_name = DEFAULT_IMG_BUCKET_S3):
    clients3 = boto3.client('s3', aws_access_key_id = Access_key_ID,
                                aws_secret_access_key = Access_secret_key)
    # img_url = "https://test-bucket-987123.s3.eu-west-1.amazonaws.com/employee/profile_img/ryj72uslh3.jpg"
    url = clients3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': bucket_name,
                                        'Key': img_path_s3,
                                    },
                                    ExpiresIn=3600)
    return url

def download_file(bucket, object_name, file_name):
    s3 = boto3.client('s3')
    s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')

def upload_pay_slip(file, pay_slip_path = DEFAULT_PAYSLIP_S3,
                    bucket = DEFAULT_IMG_BUCKET_S3):
    filename = generate_filename()
    file.filename = filename + '.' + file.filename.split('.')[-1]
    clients3 = boto3.resource('s3', aws_access_key_id = Access_key_ID,
                            aws_secret_access_key = Access_secret_key)
    my_bucket = clients3.Bucket(bucket)
    try:
        my_bucket.put_object(Key=pay_slip_path+file.filename, Body=file)
    except ClientError as e:
        logging.error(e)
        return (None, None)
    return (pay_slip_path+file.filename, bucket)

def get_pay_slips(pay_slip_path_s3,
                  bucket_name = DEFAULT_IMG_BUCKET_S3):
    clients3 = boto3.client('s3', aws_access_key_id = Access_key_ID,
                                aws_secret_access_key = Access_secret_key)
    # img_url = "https://test-bucket-987123.s3.eu-west-1.amazonaws.com/employee/profile_img/ryj72uslh3.jpg"
    url = clients3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': bucket_name,
                                        'Key': pay_slip_path_s3,
                                    },
                                    ExpiresIn=3600)
    return url

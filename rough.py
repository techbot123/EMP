import logging
import boto3
from botocore.exceptions import ClientError
from secrets import Access_key_ID, Access_secret_key
import matplotlib.image as mpimg
import io
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import requests


# from s3 import get_profile_image_s3

# return True
# def get_profile_image_s3(img_path_s3 = 'employee/profile_img/ryj72uslh3.jpg',
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
#
#
# a = get_profile_image_s3()
# plt.imshow(a)
# plt.show()
# 224039458983
clients3 = boto3.client('s3', aws_access_key_id = Access_key_ID,
                            aws_secret_access_key = Access_secret_key)
# img_url = "https://test-bucket-987123.s3.eu-west-1.amazonaws.com/employee/profile_img/ryj72uslh3.jpg"
url = clients3.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': 'test-bucket-987123',
                                    'Key': 'employee/profile_img/ryj72uslh3.jpg',
                                },
                                ExpiresIn=3600)
# clients3 = boto3.client('s3', aws_access_key_id = Access_key_ID,
#                             aws_secret_access_key = Access_secret_key)
#
# response = clients3.get_bucket_location(
#     Bucket='test-bucket-987123',
#     ExpectedBucketOwner='224039458983'
# )dataBytesIO = io.BytesIO(byteImg)
# im = Image.open(requests.get(url, stream=True).raw)
print(url)
# print(type(response.read()))

# plt.imshow(im)
# plt.show()
##################Working Fine###################
# print(user)
# pay_slips = user.pay_slips
# print(pay_slips.keys())
# for key in pay_slips.keys():
#     print(type(pay_slips[key]))
# print(type(user))
# print(type(user.pay_slips))
print(type(profile_image_url))
print()
print(profile_image_url)
# data = io.BytesIO()
# profile_image.save(data, "JPEG")
# encoded_img_data = base64.b64encode(data.getvalue())
# return render_template("user_lookup_result.html", title = 'Welc\
#                     ome Home', form = form, user_ = user_info, \
#                     profile_image = encoded_img_data.decode('utf-8'), \
#                     alt = '/static/no_profile_picture.jpeg')

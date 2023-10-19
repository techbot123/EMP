from emdb import db
col = db['user_info']
col.delete_many({})

# from emdb.models import load_user
# user = load_user('25c6bc73-5171-461e-aeaf-5aade008c468')
# print(f'user name is {user.first_name}')
# print(f'user photos is {user.photos}')
# print(f'user location is {user.location}')

# a = {}
# a['id'] = '12345'
# a['photos'] = "https://test-bucket-987123.s3.amazonaws.com/employee/profile_img/ht30kfgr2p.jpg?AWSAccessKeyId=AKIATIKOK3CT4SDY6T5L&Signature=171zB1DDvQXVO6PhYLNwcAfwWNU%3D&Expires=1642736054"
# import pickle

# b = pickle.dumps(a)
# print(pickle.loads(b))
# col.insert_one(a)
# retrieved  = col.find_one({"id":'25c6bc73-5171-461e-aeaf-5aade008c468'})
# # print(retrieved)
# user = pickle.loads(retrieved['_pickled'])
# print(user.photos)

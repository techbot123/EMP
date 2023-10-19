import time
from emdb import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pickle
import uuid
from emdb.s3 import (upload_file, get_profile_image, DEFAULT_PATH_TO_S3,
 					DEFAULT_IMG_BUCKET_S3, get_pay_slips)
from flask import flash
from geopy.geocoders import Nominatim

MONGO_COL_NAME = 'user_info'

def check_password(hash_password, password):
	return check_password_hash(hash_password, password)

@login_manager.user_loader
def load_user(id):
    print(f'in load user function with id {id} with type {type(id)}')
    user = db['user_info'].find_one({"id":id})
    # print(user)
    if not user:
        return user
    return pickle.loads(user['_pickled'])

class User(UserMixin):
    location = None
    photos = None
    disliked = set()
    matches = []
    your_likes = set()
    likes_you = set()
    hair_color = None
    hair_type = None
    eye = None
    height = None
    bod_type = None
    skin_color = None
    user_profile = None
    smoke = None
    cannabis = None
    alcohol = None
    ethnicity = None
    looking_for = None
    near_by_users = []
    near_by_users_obj = []
    swiped_users = []
    _pmessage = ''
    def __init__(self, first_name, gender, looking_for, birth_date, height,
                smoke, cannabis, alcohol, ethnicity, pvt_message,
                password, active=True, anonymous = False,
                authenticated = True):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.gender = gender
        self.looking_for = looking_for
        self.birth_date = datetime.combine(birth_date, datetime.min.time())
        self.password_hash = generate_password_hash(password)
        self.created_on = time.time()
        self.height = height
        self.smoke = smoke
        self.alcohol = alcohol
        self.cannabis = cannabis
        self.ethnicity = ethnicity
        self.pvt_message = pvt_message
        self.swiped_count = 0
        self._pickled = pickle.dumps(self)

    def create_basic_profile(self):
        user_collection = db[MONGO_COL_NAME]
        self.user_profile = {
					 'id':self.id,
					 'first_name':self.first_name,
					 'birth_date':self.birth_date,
                     'gender':self.gender,
					 'looking_for':self.looking_for,
                     'height':self.height,
                     'smoke':self.smoke,
					 'cannabis':self.cannabis,
					 'alcohol':self.alcohol,
                     'ethnicity':self.ethnicity,
					 'pvt_message':self.pvt_message,
                     'swiped_count':self.swiped_count,
					 'created_on':self.created_on,
					 'password':self.password_hash,
					 '_pickled':pickle.dumps(self)
		}
        user_collection.insert_one(self.user_profile)
        return True

    def upload_images_to_s3(self, **kwargs):
        #genearate filename for every image#
        #call upload function to s3
        user_collection = db[MONGO_COL_NAME]
        photos = {}
        for key, value in kwargs.items():
            # print(key)
            # print(value)
            if value:
                # print(value)
                s3_response = upload_file(value)
                if not s3_response[0]:
                    # return False
                    print(f'No s3 response {s3_response}')
                    return False
                else:
                    s3_path, bucket = s3_response
                    #call get profile image fucntion
                    url = get_profile_image(s3_path, bucket)
                    photos[key] = url
            else:
                print(f'key is {key} and value is {value}')
                break
        # print(f'user photos is {self.photos}')
        #store image urls in mongodb
        self.photos = photos
        # print(f'user photos is {self.photos}')
        self._pickled = pickle.dumps(self)
        # print(f'pickle object is {self._pickled}')
        # print('uploading pics to mongo ')
        user_collection.update_one({'id':self.id}, {'$set':{\
                                        'photos':self.photos,
                                        '_pickled':self._pickled
                                    }})
        return True

    def set_user_location(self, coords):
        user_collection = db[MONGO_COL_NAME]
        # print(location)
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(coords['Latitude'])+","+\
                                                    str(coords['Longitude']))
        address = location.raw['address']
        self.location = {'coords':coords,
                         'address':address}
        print(self.location)
        self._pickled = pickle.dumps(self)
        try:
            user_collection.update_one({'id':self.id}, {'$set':{\
                                                'location':self.location,
                                                '_pickled':self._pickled
                                            }})
            print('success')
            return True
        except Exception as e:
            print(f'Encountered the following error while setting user location\
                                                                    : {error}')
        return False

    def get_users_by_city(self):
        user_collection = db[MONGO_COL_NAME]
        near_by_users = user_collection.find({
          "location.address.country_code":self.location['address']['country_code'],
          "location.address.state":self.location['address']['state'],
          "location.address.city":self.location['address']['city']
                                    })
        print('printing near by users')
        for i, item in enumerate(near_by_users):
            # print(pickle.loads(item['_pickled']))
            # print(item)
            # print()
            if i == 100:
                break
            self.near_by_users_obj.append(pickle.loads(item['_pickled']))
            self.near_by_users.append(item['id'])
        print(self.near_by_users)
        self._pickled = pickle.dumps(self)
        # try:
        user_collection.update_one({'id':self.id}, {'$set':{\
                                            'near_by_users':self.near_by_users,
                                            '_pickled':self._pickled
                                        }})
        return True
        # except Exception as error:
        #     print(f'Encountered the following error while getting near by users\
        #                                                             : {error}')
        #     return False

    def update_mongo_db(self, entity):
        self._pickled = pickle.dumps(self)
        user_collection = db[MONGO_COL_NAME]
        update_items = {}
        for item in entity:
            val = getattr(self, item)
            if type(val) == set:
                update_items[item] = list(val)
            else:
                update_items[item] = val
        update_items['_pickled'] = self._pickled
        user_collection.update_one({'id':self.id},\
                                            {'$set':update_items})

    def get_users_by_looking_for(self):
        pass

    def get_id(self):
        return self.id

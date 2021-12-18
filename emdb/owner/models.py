# import os
import time
from emdb import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pickle
import uuid
# from emdb.routes import login_manager

def check_password(hash_password, password):
	return check_password_hash(hash_password, password)

@login_manager.user_loader
def load_user(id):
	print(f'in load user function with id {id} with type {type(id)}')
	u = db['user_info'].find_one({"id":id})
	print(u)
	return pickle.loads(u['_pickeld'])

class Owner(UserMixin):
	def __init__(self, active=True, anonymous = False,\
	 			authenticated = True):
		self.id  = None
		self.first_name = None
		self.last_name = None
		self.email_id = None
		self.address_line_1 = None
		self.address_line_2 = None
		self.city = None
		self.state = None
		self.zipcode = None
		self.phone = None
		self.birth_date = None
		self.password_hash = None
		self.created_on = None
		self.myself = None
		self.user_profile = None
		self.role = None
		self.profile_image = None
        self.reports_to = None
        self.reported_by = []

	def create_user_profile(self, first_name, last_name,
							email_id, address_line_1, address_line_2, city,
                            state, zipcode, phone, birth_date, password,
                            profile_image = profile_image
                            ):
		user_col = db['user_info']
		if user_col.find_one({'email_id':email_id}):
			print('Email id already exists!')
			return False
		else:
			self.id = str(uuid.uuid4())
			self.first_name = first_name
			self.last_name = last_name
			self.email_id = email_id
			self.address_line_1 = address_line_1
            self.address_line_2 = address_line_2
            self.city = city
            self.state = state
            self.zipcode = zipcode
            self.profile_image = profile_image
			self.phone = phone
			self.birth_date = datetime.combine(birth_date, datetime.min.time())
			self.password_hash = generate_password_hash(password)
			self.created_on = time.time()
			self.user_profile = {
								 'id':self.id,
								 'first_name':self.first_name,
								 'last_name':self.last_name,
								 'email_id':self.email_id,
								 'address_line_1':self.address_line_1,
                                 'address_line_2':self.address_line_2,
                                 'city':self.city,
                                 'state':self.state,
                                 'zipcode':self.zipcode,
								 'phone':self.phone,
								 'birth_date':self.birth_date,
								 'created_on':self.created_on,
								 'password':self.password_hash,
                                 'role':self.role,
                                 'profile_image':self.profile_image,
                                 'reports_to':self.reports_to,
                                 'reported_by':self.reported_by,
								 '_pickeld':pickle.dumps(self)
								}
			# self.myself = self

			user_col.insert_one(self.user_profile)
			return True

	# def __repr__(self):
	# 	print(f'User\'s first name is {self.first_name} and last name is {self.last_name}')

	def employee_lookup_info(self):
		return {
		'First Name':self.first_name,
		'Last Name':self.last_name,
		'Email':self.email_id,
		'Phone':self.phone
			}

	def get_id(self):
		print(f'my id is {self.id}')
		return self.id



class User(Employee, UserMixin):
	def __init__(self, id, active=True, anonymous = False,\
	 			authenticated = True):
		self.id  = id

	def load_user_data(self, json_data):
		# first_name
		if json_data:
			self.first_name = json_data['first_name']
			self.last_name = json_data['last_name']
			self.email_id = json_data['email_id']
			self.address = json_data['address']
			self.phone = json_data['phone']
			self.birth_date = json_data['birth_date']
			self.password_hash = json_data['password']
			self.created_on = json_data['created_on']

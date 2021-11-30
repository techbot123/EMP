# import os
import time
# print(time.time())
class Employee():
	emails = []
	def __init__(self,
				 f_name,
				 l_name,
				 email_id,
				 address,
				 phone,
				 birth_date
				 ):
		self.first_name = f_name
		self.last_name = l_name
		self.email_id = email_id
		self.address = address
		self.phone = phone
		self.birth_date = birth_date
		self.created_on = time.time()
		self.user_profile = None
		self.create_user_profile_for_json()
		self.update_email()


	def print_user_profile(self):
		print(self.first_name, self.last_name, self.created_on)

	def update_email(self):
		# print('here')
		# nonlocal emails
		self.emails.append(self.email_id)
		# self.user_count += 1

	def create_user_profile_for_json(self):
		# print('here as well')
		self.user_profile = {'first_name':self.first_name,
							 'last_name':self.last_name,
							 'email_id':self.email_id,
							 'address':self.address,
							 'phone':self.phone,
							 'birth_date':self.birth_date,
							 'created_on':self.created_on,
							}






	




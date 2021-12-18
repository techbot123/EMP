# import os
import time
from emdb import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pickle
import uuid
from emdb.models import Employee


class Owner(Employee, UserMixin):

	def set_employee_pay(self, email_id, pay):
		try:
			employee = db['user_info'].find_one({'email_id':email_id})
		except:
			print('Error fetching user!')
			return False
		employee = pickle.loads(employee['_pickled'])
		employee.pay = pay
		print(employee.__class__)
		print(employee.employee_lookup_info())
		print(employee.pay)
		# employee['_pickled'] = pickle.dumps(employee)
		db['user_info'].update_one({'email_id':email_id},
			{'$set':{'pay':pay, '_pickled':pickle.dumps(employee)}})
		return True

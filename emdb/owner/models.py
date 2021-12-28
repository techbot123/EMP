# import os
import time
from emdb import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pickle
import uuid
from emdb.models import Employee
from datetime import datetime
from flask import flash
from emdb.s3 import upload_pay_slip

def load_user_by_email(email_id):
	try:
		employee = db['user_info'].find_one({'email_id':email_id})
	except Exception as e:
		print('Error fetching user!')
		flash('Employee not found!!', 'danger')
		return None
	return pickle.loads(employee['_pickled'])

class Owner(Employee, UserMixin):

	def set_employee_pay(self, email_id, pay):
		if (employee := load_user_by_email(email_id)):
			employee.pay[datetime.today().strftime('%Y-%m-%d')] = pay
			try:
				db['user_info'].update_one({'email_id':email_id},
					{'$set':{'pay':employee.pay,\
					 '_pickled':pickle.dumps(employee)}})
				return True
			except Exception as e:
				print(e)
				flash(f'Database error!', 'danger')
				return False

	def upload_employee_pay_slips(self, email_id, file):
		if (employee := load_user_by_email(email_id)):
			#upload pay slip file into S3
			s3_response = upload_pay_slip(file)
			if not s3_response[0]:
				flash(f'Could not upload pay slip!', 'danger')
				return False
			else:
				pay_slip_dict = {'pay_slip_path':s3_response[0],
								 'bucket':s3_response[1]
								 }
				employee.pay_slips[datetime.today().strftime('%Y-%m-%d')] = pay_slip_dict
				try:
					db['user_info'].update_one({'email_id':email_id},
										{'$set':{'pay_slips':employee.pay_slips,
										'_pickled':pickle.dumps(employee)}})
					flash('Employee pay slip uploaded successfully!', 'success')
					return True
				except Exception as e:
					print(e)
					flash(f'Mongo DB error!', 'danger')
					return False
		else:
			flash('Could not find employee!', 'danger')
			return False

	def increment_pay(self, email_id, inc):
		if (employee := load_user_by_email(email_id)):
			employee.pay[datetime.today().strftime('%Y-%m-%d')] = \
				float(employee.pay[max(employee.pay.keys())]) + ((float(inc) * \
				float(employee.pay[max(employee.pay.keys())]))/100.0)
			try:
				db['user_info'].update_one({'email_id':email_id},
										{'$set':{'pay':employee.pay,
										'_pickled':pickle.dumps(employee)}})
				flash('Employee pay incremented successfully!', 'success')
				return True
			except Exception as e:
				print(e)
				flash(f'Mongo DB error!', 'danger')
				return False
		else:
			flash('Could not find employee!', 'danger')
			return False

	def decrement_pay(self, email_id, inc):
		if (employee := load_user_by_email(email_id)):
			employee.pay[datetime.today().strftime('%Y-%m-%d')] = \
				float(employee.pay[max(employee.pay.keys())]) - ((float(inc) * \
				float(employee.pay[max(employee.pay.keys())]))/100.0)
			try:
				db['user_info'].update_one({'email_id':email_id},
										{'$set':{'pay':employee.pay,
										'_pickled':pickle.dumps(employee)}})
				flash('Employee pay decremented successfully!', 'success')
				return True
			except Exception as e:
				print(e)
				flash(f'Mongo DB error!', 'danger')
				return False
		else:
			flash('Could not find employee!', 'danger')
			return False

	def set_employee_hire_date(self, email_id, hire_date):
		if (employee := load_user_by_email(email_id)):
			# print(hire_date.strptime('%Y-%m-%dT%H:%M:%S.%fZ'))
			print(datetime.combine(hire_date, datetime.min.time()))
			employee.hire_date = datetime.combine(hire_date, datetime.min.time())
			try:
				db['user_info'].update_one({'email_id':email_id},
										{'$set':{'hire_date':employee.hire_date,
										'_pickled':pickle.dumps(employee)}})
				flash('Employee hire date set successfully!', 'success')
				return True
			except Exception as e:
				flash(f'Error with Database!', 'danger')
				return False
		else:
			flash('Could not find employee!', 'danger')
			return False

	def set_employee_bonus(self, email_id, bonus):
		if (employee := load_user_by_email(email_id)):
			employee.bonus[datetime.today().strftime('%Y-%m-%d')] = bonus
			try:
				db['user_info'].update_one({'email_id':email_id},
					{'$set':{'bonus':employee.bonus,\
					 '_pickled':pickle.dumps(employee)}})
				return True
			except Exception as e:
				print(e)
				flash(f'Database error!', 'danger')
				return False

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
	except:
		print('Error fetching user!')
		flash('Employee not found!!', 'danger')
		return None
	return pickle.loads(employee['_pickled'])

class Owner(Employee, UserMixin):

	def set_employee_pay(self, email_id, pay):
		if (employee := load_user_by_email(email_id)):
			employee.pay = pay
			db['user_info'].update_one({'email_id':email_id},
				{'$set':{'pay':pay, '_pickled':pickle.dumps(employee)}})
			flash('Pay set successfully!', 'success')
			return True
		else:
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
				db['user_info'].update_one({'email_id':email_id},
									{'$set':{'pay_slips':employee.pay_slips,
									'_pickled':pickle.dumps(employee)}})
				flash('Employee pay slip uploaded successfully!', 'success')
				return True
		else:
			flash('Could not find employee!', 'danger')
			return False

	def increment_pay(self, email_id, inc):
		if (employee := load_user_by_email(email_id)):
			employee.pay = float(employee.pay) + ((float(inc) * \
						   							float(employee.pay))/100.0)
			db['user_info'].update_one({'email_id':email_id},
									{'$set':{'pay':employee.pay,
									'_pickled':pickle.dumps(employee)}})
			flash('Employee pay incremented successfully!', 'success')
			return True
		else:
			return False

	def decrement_pay(self, email_id, inc):
		if (employee := load_user_by_email(email_id)):
			employee.pay = float(employee.pay) - ((float(inc) * \
						   							float(employee.pay))/100.0)
			db['user_info'].update_one({'email_id':email_id},
									{'$set':{'pay':employee.pay,
									'_pickled':pickle.dumps(employee)}})
			flash('Employee pay decremented successfully!', 'success')
			return True
		else:
			return False

from flask import render_template, request, url_for, flash, redirect
from emdb.models import Employee
from emdb import app, mongoclient
from emdb.forms import RegistrationForm, LoginForm
from emdb.new_reg_form import NewRegistrationForm
from emdb.mongo_connector import MongoCon
from functools import wraps
import json
import os

PATH_TO_LDB = '/Users/skattish/Documents/DBMS/db_files/'

def decorator_func(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
            print(f'Decorating {func.__name__} function...')
            return func(*args, **kwargs)
      return wrapper

@decorator_func
def write_to_file(emp_obj):
      num_files = len(os.listdir(PATH_TO_LDB))
      with open(PATH_TO_LDB + 'user_file'+str(num_files + 1) + '.json', 'w') as outfile:
            json.dump(emp_obj, outfile)

def validate_user(email):
      emps = RegistrationForm()
      print(f'heres the list of all employess : {emps.users}')
      return email in set().union(*(user.keys() for user in emps.users))

@app.route('/')
@app.route('/login', methods = ["POST", "GET"])
@decorator_func
def login():
      return render_template("login.html", title = 'Log in or Register')

# @app.route('/after_login', methods = ["POST"])
# @decorator_func
# def after_login():
#       # user_det = LoginForm()
#       # user_det.get_login_details()
#       if validate_user(user_det.email_id):
#             return render_template("after_login.html", title = 'Logged in')
#       else:
#             return render_template("invalid_signin.html", title='chutiye')

@app.route('/after_login', methods = ["GET"])
@decorator_func
def after_login():
      # user_det = LoginForm()
      # user_det.get_login_details()
      # if validate_user(user_det.email_id):
      return render_template("after_login.html", title = 'Logged in')
      # else:
      #       return render_template("invalid_signin.html", title='chutiye')

# @app.route('/register')
# @decorator_func
# def register():
#       return render_template("register.html", title = 'Register')

@app.route('/register', methods = ['GET', 'POST'])
@decorator_func
def register():
      print('at register function')
      form = NewRegistrationForm()
      if form.validate_on_submit():
            print('Validated User!')
            flash(f'Account created for {form.first_name.data} successfully!', 'success')
            return redirect(url_for('login'))
      return render_template("new_register.html", title = 'Register', form = form)

# @decorator_func
# @app.route('/form', methods = ["POST"])
# def form():
#       reg_new_user = RegistrationForm()
#       reg_new_user.get_registration_details()

#       employee = Employee(reg_new_user.f_name, reg_new_user.l_name, reg_new_user.email, str(reg_new_user.address1 + reg_new_user.address2 +\
#                   reg_new_user.city + reg_new_user.state + str(reg_new_user.zipcode)), reg_new_user.phone, reg_new_user.birth_date)
#       print(employee.user_profile)
#       # write_to_file(employee.user_profile)
#       reg_new_user.users.append({reg_new_user.email:employee})
#       # db = mongoclient['Employee']
#       # collection = db['user_info']
#       # # print(f'Inserting user details in MongoDB! User profile is : {employee.user_profile}')
#       # collection.insert_one(employee.user_profile)

#       return render_template("form.html", name = employee.first_name)

@decorator_func
@app.route('/form', methods = ["POST"])
def form():
      reg_new_user = NewRegistrationForm()
      # reg_new_user.get_registration_details()

      # employee = Employee(reg_new_user.f_name, reg_new_user.l_name, reg_new_user.email, str(reg_new_user.address1 + reg_new_user.address2 +\
      #             reg_new_user.city + reg_new_user.state + str(reg_new_user.zipcode)), reg_new_user.phone, reg_new_user.birth_date)
      # print(employee.user_profile)
      # # write_to_file(employee.user_profile)
      # reg_new_user.users.append({reg_new_user.email:employee})
      # db = mongoclient['Employee']
      # collection = db['user_info']
      # # print(f'Inserting user details in MongoDB! User profile is : {employee.user_profile}')
      # collection.insert_one(employee.user_profile)

      return render_template("form.html", name = reg_new_user.first_name)






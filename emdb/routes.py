from flask import render_template, request, url_for, flash, redirect

from emdb import app, db, login_manager
import flask_login
from emdb.forms import RegistrationForm, LoginForm
from emdb.mongo_connector import MongoCon
from functools import wraps
import json
import os
from flask_login import login_user, login_required, logout_user, fresh_login_required
from emdb.models import Employee, check_password, User
from werkzeug.utils import secure_filename
import pickle
from emdb.owner.models import Owner


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

@app.route('/home', methods = ["GET", "POST"])
@decorator_func
def home():
    print('in main home')
    print(flask_login.current_user.__class__)
    if isinstance(flask_login.current_user, Owner):
        print('user is owner')
        return redirect(url_for('owners.home'))
    elif isinstance(flask_login.current_user, Employee):
        print('user is emploeyy')
        return redirect(url_for('employees.home'))
    print(flask_login.current_user.__class__)
    return redirect(url_for('owners.home'))

@app.route('/')
@app.route('/login', methods = ["GET", "POST"])
@decorator_func
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print('Login form validated!')
        user = db['user_info'].find_one({"email_id": form.email_id.data})
        if user is not None and check_password(user['password'], form.password.data):
            user_ = pickle.loads(user['_pickled'])
            login_user(user_)
            flash('Successful login!', 'success')
            if isinstance(user_, Owner):
                return redirect(url_for('owners.home'))
            elif isinstance(user_, Employee):
                return redirect(url_for('employees.home'))
        elif not user:
            flash('The email you entered isn’t connected to an account. Find your account and log in.', 'danger')
            return redirect(url_for('login'))
        else:
            flash('Email ID or Password incorrect!', 'danger')
            return redirect(url_for('login'))
    return render_template("login.html", title = 'Log in or Register', form = form)

@app.route('/register', methods = ['GET', 'POST'])
@decorator_func
def register():
      print('at register function')
      form = RegistrationForm()
      if form.validate_on_submit():
            print('Validated User!')
            if form.email_id.data == 'sagarck44@gmail.com':
                employee = Owner()
            else:
                employee = Employee()
            print(f'In register func and the class is {employee.__class__}')
            # print(form.profile_image.data.filename, type(form.profile_image.data))
            profile_image = form.profile_image.data
            print(profile_image)
            # print(profile_image.__name__)
            if employee.create_user_profile(form.first_name.data, \
                form.last_name.data, form.email_id.data, form.address_line_1.data,
                form.address_line_2.data, form.city.data, form.state.data,
                str(form.zipcode.data), form.phone.data, form.birth_date.data,
                form.password.data, profile_image = profile_image):
                flash(f'Account created for {form.first_name.data} successfully!', 'success')
            else:
                flash(f'Email ID already exists!', 'danger')
            return redirect(url_for('login'))
      return render_template("register.html", title = 'Register', form = form)

@app.route('/logout')
@decorator_func
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('login'))

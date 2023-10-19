from flask import render_template, request, url_for, flash, redirect, jsonify
from emdb import app, db, login_manager
import flask_login
from emdb.forms import RegistrationForm, LoginForm, UploadPhotosForm, PersonalUserInfo
from emdb.mongo_connector import MongoCon
from functools import wraps
import json
import os
from flask_login import login_user, login_required, logout_user, fresh_login_required
from emdb.models import User, check_password, load_user
from werkzeug.utils import secure_filename
import pickle
from emdb.owner.models import Owner

def decorator_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Decorating {func.__name__} function...')
        return func(*args, **kwargs)
    return wrapper

def logout_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logout_user()
        return func(*args, **kwargs)
    return wrapper

@app.route('/home', methods = ["GET", "POST"])
@decorator_func
def home():
    print('in main home')
    # current_user = load_user(flask_login.current_user.id)
    print(flask_login.current_user.__class__)
    if isinstance(flask_login.current_user, Owner):
        print('user is owner')
        return redirect(url_for('owners.home'))
    elif isinstance(flask_login.current_user, User):
        print('user is emploeyy')
        return redirect(url_for('employees.home'))
    print(flask_login.current_user.__class__)
    return redirect(url_for('owners.home'))

@app.route('/')
@app.route('/login', methods = ["GET", "POST"])
@decorator_func
@logout_decorator
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
            elif isinstance(user_, User):
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
            user = User(form.first_name.data, form.gender.data,\
                form.looking_for.data, form.birth_date.data,form.height.data,
                form.smoke.data, form.cannabis.data,form.alcohol.data,
                form.ethnicity.data, form.pvt_message.data,form.password.data)
            if user.create_basic_profile():
                flash(f'Account created for {form.first_name.data} successfully!', 'success')
                login_user(user)
                return redirect(url_for('user_location',coords = {}, code=307))
            else:
                flash(f'Email ID already exists!', 'danger')
                return redirect(url_for('login'))
      return render_template("register.html", title = 'Register', form = form)

@app.route('/user_location', methods = ['GET', 'POST'])
@decorator_func
def user_location():
    return render_template('geolocation.html', title = 'set location')

@app.route("/postlocation", methods = ['POST', 'GET'])
def postmethod():
    location = request.get_json()
    current_user = load_user(flask_login.current_user.id)
    print(type(current_user))
    if current_user.set_user_location(location):
        return jsonify(location)
    else:
        flash(f'Location Error!', 'danger')
        return 404
    print(location)
    return jsonify(location)

@app.route('/upload_user_pictures', methods = ['GET', 'POST'])
@decorator_func
def upload_user_pictures():
    print('here')
    form = UploadPhotosForm()
    if form.validate_on_submit():
        current_user = load_user(flask_login.current_user.id)
        if current_user.upload_images_to_s3(profile_image = form.profile_image.data,\
                          image1 = form.image1.data, image2 = form.image2.data,
                          image3 = form.image3.data, image4 = form.image4.data,
                          image5 = form.image5.data):
            flash(f'images uploaded successfully!', 'success')
            return redirect(url_for('.home', current_user = current_user))
        else:
            flash(f'images did not get uploaded!', 'danger')
        return redirect(url_for('.login'))
    return render_template("upload_user_images.html", title = 'Upload photos',\
                                                                    form = form)

@app.route('/logout')
@decorator_func
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('login'))

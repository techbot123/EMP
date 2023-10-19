from flask import Blueprint, render_template, redirect, url_for, request
from emdb import db, login_manager
from emdb.employee.user_lookup_form import (UserLookupForm, ChangePersonalInfo,
                                                                    SearchBox)
from emdb.models import User, load_user
import pickle
from emdb.routes import decorator_func
import flask_login
from flask_login import login_required, fresh_login_required
from emdb.employee.contact_change_form import (AddressChangeForm, PhoneChangeForm,
                                            EmailChangeForm, ProfileImageChange)
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import io
from emdb.s3 import upload_file, NO_IMG_S3, DEFAULT_IMG_BUCKET_S3


employee_b = Blueprint('employees', __name__,
                template_folder = 'templates/employee', static_folder='static')

@decorator_func
def user_like(current_user):
    #get the recent user
    end_user = load_user(current_user.swiped_users[-1])
    #cehck if the user is in likes you list
    if end_user.id in current_user.likes_you:
        #if yes add the user to matched list
        #update the match list on the user end
        current_user.matches.append(end_user.id)
        end_user.matches.append(current_user.id)
        #remove users from likes you list
        current_user.likes_you.remove(end_user.id)
        end_user.likes_you.remove(current_user.id)
    else:
        print('no mutual likes')
        current_user.your_likes.add(end_user.id)
        end_user.likes_you.add(current_user.id)
    #update mongo db
    current_user.update_mongo_db(['matches', 'likes_you', 'your_likes'])
    end_user.update_mongo_db(['matches', 'likes_you', 'your_likes'])

@decorator_func
def user_dislike(current_user):
    #get the recent swiped user
    end_user = load_user(current_user.swiped_users[-1])
    #check if end user is in like_you list
    if end_user.id in current_user.likes_you:
        #if yes then remove that user from likes_you
        current_user.likes_you.remove(end_user.id)
    else:
        #if no then add the current user in disliked set of end_user
        end_user.disliked.add(current_user.id)
    current_user.update_mongo_db(['likes_you'])
    end_user.update_mongo_db(['disliked'])

@employee_b.route('/home', methods = ['POST', 'GET'])
@decorator_func
@login_required
def home():
    current_user = load_user(flask_login.current_user.id)
    form = SearchBox()
    if current_user.get_users_by_city():
        if form.validate_on_submit():
            #Apply filters
            print('here')
            search_query = form.search_box.data
            print(search_query)
            if form.like.data:
                user_like(current_user)
            elif form.dislike.data:
                user_dislike(current_user)
        #check if the person has been swiped before
        for user in current_user.near_by_users:
            print(f'user is {user}')
            if (user in current_user.swiped_users) or (user in current_user.disliked)\
                                                     or (user == current_user.id):
                continue
            else:
                #Add user to swiped list
                current_user.swiped_users.append(user)
                #Load the user id
                user_ = load_user(user)
                #show the person's photos
                user_photos = user_.photos
                user_name = user_.first_name
                print(f'user is {user_}')
                print(f'user name is : {user_name}')
                print(f'user photos is " {user_photos}"')
                return render_template("employee_home.html", title = 'Home',\
                                            form = form, user_ = user_photos)

@employee_b.route('/user_lookup', methods = ['POST', 'GET'])
@decorator_func
@login_required
def user_lookup():
    form = UserLookupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            users = db['user_info'].find({"first_name": form.search_name.data})
            if users:
                user_dict = {}
                for i, user in enumerate(users):
                    # print(f'printing user {user}')
                    user = pickle.loads(user['_pickled'])
                    user_dict[str(i)] = user.employee_lookup_info()
                return render_template("user_lookup_result.html", title = 'Welc\
                                    ome Home', form = form, user_ = user_dict, \
                                    # profile_image = profile_image_url, \
                                    alt = '/static/no_profile_picture.jpeg')
            else:
                return render_template("user_lookup_result.html", title = 'Welco\
                                              me Home', form = form, user_=None)
        else:
            return render_template("user_lookup.html", title = 'Welcome Home',\
                                                                    form = form)
    else:
        return render_template("user_lookup.html", title = 'Welcome Home',\
                                                                    form = form)

@employee_b.route('/personal_info', methods = ['POST', 'GET'])
@decorator_func
@login_required
def personal_info():
    form = ChangePersonalInfo()
    current_user_dict = db['user_info'].find_one({"id": flask_login.current_user.id})
    current_user = pickle.loads(current_user_dict['_pickled'])
    # print(f'user email is {current_user.email_id}')
    if form.validate_on_submit():
        print('form validated')
        if form.address.data:
            print('you chose address')
            return redirect(url_for('.personal_info_address_change'))
        elif form.phone.data:
            print('you chose phone')
            return redirect(url_for('.personal_info_phone_change'))
        elif form.email.data:
            print('you chose email')
            return redirect(url_for('.personal_info_email_change'))
        elif form.profile_image.data:
            print('you chose profile image')
            return redirect(url_for('.personal_info_profile_image_change'))
        elif form.pay_slips.data:
            print('you chose to view your pay')
            return redirect(url_for('.view_pay_slips'))
        else:
            return redirect(url_for('.personal_info'))
    else:
        return render_template("personal_info_change.html", title = 'Personal \
        Information - EM', form = form)

@employee_b.route('/personal_info_address_change', methods = ['GET', 'POST'])
@decorator_func
@fresh_login_required
def personal_info_address_change():
    form = AddressChangeForm()
    user = load_user(flask_login.current_user.id)
    _user_email = user.email_id
    _user_address = str(user.address_line_1) + ' ' + str(user.address_line_2) +\
                ' ' + str(user.city) + ' ' + str(user.state) + ' ' +\
                str(user.zipcode)
    if form.validate_on_submit():
        user.address_line_1 = form.address_line_1.data
        user.address_line_2 = form.address_line_2.data
        user.city = form.city.data
        user.state = form.state.data
        user.zipcode = form.zipcode.data
        user._pickled = pickle.dumps(user)
        db['user_info'].update_one({'email_id':_user_email}, {'$set':{\
                                        'address_line_1':user.address_line_1,
                                        'address_line_2':user.address_line_2,
                                        'city':user.city,
                                        'state':user.state,
                                        'zipcode':user.zipcode,
                                        '_pickled':user._pickled
                                    }})
        return redirect(url_for('.personal_info'))
    else:
        return render_template("address_change.html", title = 'Change your \
                            address - EM', form = form, address = _user_address)


@employee_b.route('/personal_info_phone_change', methods = ['GET', 'POST'])
@decorator_func
@fresh_login_required
def personal_info_phone_change():
    form = PhoneChangeForm()
    user = load_user(flask_login.current_user.id)
    _user_email = user.email_id
    _user_phone = user.phone
    if form.validate_on_submit():
        user.phone = form.phone.data
        user._pickled = pickle.dumps(user)
        db['user_info'].update_one({'email_id':_user_email}, {'$set':{\
                                                        'phone':form.phone.data,
                                                        '_pickled':user._pickled}})

        return redirect(url_for('.personal_info'))
    else:
        return render_template("phone_change.html", title = 'Change your \
                            phone - EM', form = form, phone = _user_phone)

@employee_b.route('/personal_info_email_change', methods = ['GET', 'POST'])
@decorator_func
@fresh_login_required
def personal_info_email_change():
    form = EmailChangeForm()
    user = load_user(flask_login.current_user.id)
    _user_email = user.email_id
    if form.validate_on_submit():
        user.email_id = form.email_id.data
        user._pickled = pickle.dumps(user)
        db['user_info'].update_one({'email_id':_user_email}, {'$set':{\
                                                        'email_id':user.email_id,
                                                        '_pickled':user._pickled}})
        return redirect(url_for('.personal_info'))
    else:
        return render_template("email_change.html", title = 'Change your \
                            email - EM', form = form, email = _user_email)


@employee_b.route('/personal_info_profile_image_change', methods = ['GET', 'POST'])
@decorator_func
@fresh_login_required
def personal_info_profile_image_change():
    form = ProfileImageChange()
    user = load_user(flask_login.current_user.id)
    _user_email = user.email_id
    if form.validate_on_submit():
        profile_image = form.profile_image.data
        print(profile_image)
        if profile_image:
            print('here in profile image change')
            sto_det = upload_file(profile_image)
            if sto_det:
                filenames3, bucket = sto_det
                print(f'filename is {filenames3} and bucket is {bucket}')
                profile_det = {'file_path':filenames3,
                               'bucket_name':bucket
                               }
                user.profile_image = profile_det
        else:
            user.profile_image = {'file_path':NO_IMG_S3,
                                  'bucket_name':DEFAULT_IMG_BUCKET_S3
                                 }
        print(user.profile_image)
        # user.profile_image = profile_image
        user._pickled = pickle.dumps(user)
        db['user_info'].update_one({'email_id':_user_email}, {'$set':{\
                                            'profile_image':user.profile_image,
                                            '_pickled':user._pickled}})
        return redirect(url_for('.personal_info'))
    else:
        return render_template("profile_image_change.html", title = 'Change your \
                            profile picture - EM', form = form)


@employee_b.route('/view_pay_slips', methods = ['GET', 'POST'])
@decorator_func
@fresh_login_required
def view_pay_slips():
    user = load_user(flask_login.current_user.id)
    results = user.employee_pay_slip_lookup()
    if not results:
        return redirect(url_for('home'))
    else:
        return render_template("employee_pay_slips.html", pay_slips = results)

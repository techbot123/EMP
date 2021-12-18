from flask import Blueprint, render_template, redirect, url_for, request
from emdb import db, login_manager
from emdb.employee.user_lookup_form import UserLookupForm, ChangePersonalInfo
from emdb.models import Employee, load_user
import pickle
from emdb.routes import decorator_func
import flask_login
from flask_login import login_required, fresh_login_required
from emdb.employee.contact_change_form import (AddressChangeForm, PhoneChangeForm,
                                                                EmailChangeForm)

employee_b = Blueprint('employees', __name__,
                                template_folder = 'templates/employee')

@employee_b.route('/user_lookup', methods = ['POST', 'GET'])
@decorator_func
@login_required
def user_lookup():
    form = UserLookupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db['user_info'].find_one({"first_name": form.search_name.data})
            if user:
                user = pickle.loads(user['_pickeld'])
                print(f'printing lookup user info: {user.employee_lookup_info()}')
                user = user.employee_lookup_info()
                print(user)
                return render_template("user_lookup_result.html", title = 'Welc\
                                           ome Home', form = form, user_ = user)
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
    # user = flask_login.current_user
    # user = load_user(flask_login.current_user.id)
    current_user_dict = db['user_info'].find_one({"id": flask_login.current_user.id})
    current_user = pickle.loads(current_user_dict['_pickled'])
    print(f'user email is {current_user.email_id}')
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
        #Update current user address from form
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
        # print(f'new email is {new_email}')
        db['user_info'].update_one({'email_id':_user_email}, {'$set':{\
                                                        'email_id':user.email_id,
                                                        '_pickled':user._pickled}})
        return redirect(url_for('.personal_info'))
    else:
        return render_template("email_change.html", title = 'Change your \
                            email - EM', form = form, email = _user_email)

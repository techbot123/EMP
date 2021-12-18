from flask import Blueprint, render_template, redirect, url_for, request, flash
from emdb import db, login_manager
from emdb.employee.user_lookup_form import UserLookupForm, ChangePersonalInfo
from emdb.models import Employee, load_user
import pickle
from emdb.routes import decorator_func
import flask_login
from flask_login import login_required, fresh_login_required
# from emdb.employee.contact_change_form import (AddressChangeForm, PhoneChangeForm,
#                                                EmailChangeForm, ProfileImageChange)
from emdb.owner.owner_forms import EmployeeEmailSearch

owner_b = Blueprint('owners', __name__,
                                template_folder = 'templates/owner')

@owner_b.route('/owners/home')
@decorator_func
@login_required
def home():
    print('owners home')
    return render_template("owner_home.html", title = 'Home')

@owner_b.route('/set_pay', methods = ['POST', 'GET'])
@decorator_func
@login_required
def set_pay():
    form = EmployeeEmailSearch()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user = load_user(flask_login.current_user.id)
            if current_user.set_employee_pay(form.email_id.data, form.pay.data):
                flash('Pay entered successfully!', 'success')
            else:
                flash('Pay entered unsuccessfully!', 'danger')
            return render_template("owner_home.html", title = 'Welcome Home')
    else:
        return render_template("user_pay_set.html", title = 'Welcome Home',\
                                                                    form = form)

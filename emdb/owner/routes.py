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
from emdb.owner.owner_forms import (EmployeePaySet, EmployeeUploadPaySlip,
                                EmployeeIncrementPay, EmployeeDecrementPay)
from werkzeug.utils import secure_filename

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
    form = EmployeePaySet()
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

@owner_b.route('/upload_payslips', methods = ['GET', 'POST'])
@decorator_func
@login_required
def upload_payslips():
    form = EmployeeUploadPaySlip()
    # if request.method == 'POST':
    if form.validate_on_submit():
        current_user = load_user(flask_login.current_user.id)
        print(form.pay_slip.data, type(form.pay_slip.data))
        print(form.email_id.data)
        pay_slip = form.pay_slip.data
        print()
        if pay_slip:
            if current_user.upload_employee_pay_slips(form.email_id.data,
                                                  pay_slip):
                print('Success!')
            else:
                print('Fail')
        else:
            flash('File upload error!', 'danger')
        return redirect(url_for('owners.home'))
    else:
        return render_template("pay_slip_upload.html", title = 'Welcome Home',\
                                                                    form = form)

@owner_b.route('/increment_employee_pay', methods = ['POST', 'GET'])
@decorator_func
@login_required
def increment_employee_pay():
    form = EmployeeIncrementPay()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user = load_user(flask_login.current_user.id)
            if current_user.increment_pay(form.email_id.data,
                                                      form.inc.data):
                print('Success!')
            else:
                print('Fail')
                flash('Error Incrementing!', 'danger')
            return redirect(url_for('owners.home'))
    else:
        return render_template("increment_pay.html", title = 'Welcome Home',\
                                                                    form = form)

@owner_b.route('/decrement_employee_pay', methods = ['POST', 'GET'])
@decorator_func
@login_required
def decrement_employee_pay():
    form = EmployeeDecrementPay()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user = load_user(flask_login.current_user.id)
            if current_user.decrement_pay(form.email_id.data,
                                                      form.dec.data):
                print('Success!')
            else:
                print('Fail')
                flash('Error Decrementing!', 'danger')
            return redirect(url_for('owners.home'))
    else:
        return render_template("decrement_pay.html", title = 'Welcome Home',\
                                                                    form = form)

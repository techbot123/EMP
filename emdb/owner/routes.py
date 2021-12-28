from flask import Blueprint, render_template, redirect, url_for, request, flash
from emdb import db, login_manager
from emdb.employee.user_lookup_form import UserLookupForm, ChangePersonalInfo
from emdb.models import Employee, load_user
import pickle
from emdb.routes import decorator_func
import flask_login
from flask_login import login_required, fresh_login_required
from functools import wraps
from emdb.owner.models import Owner
from emdb.owner.owner_forms import (EmployeePaySet, EmployeeUploadPaySlip,
        EmployeeIncrementPay, EmployeeDecrementPay,EmployeePaySetConfirmation,
        EmployeeBonusSet, EmployeeSetHireDate)
from werkzeug.utils import secure_filename

owner_b = Blueprint('owners', __name__,
                                template_folder = 'templates/owner')

def owner_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = load_user(flask_login.current_user.id)
        if isinstance(current_user, Owner):
            return func(*args, **kwargs)
        else:
            flash(f'You dont have access to this page!', 'danger')
            return redirect(url_for('employees.home'))
    return wrapper

@owner_b.route('/owners/home')
@decorator_func
@owner_required
@login_required
def home():
    print('owners home')
    return render_template("owner_home.html", title = 'Home')

@owner_b.route('/set_pay', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def set_pay():
    form = EmployeePaySet()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('.confirm_pay_window', \
                            email_id = form.email_id.data, pay = form.pay.data))
        else:
            flash(f'Make sure you entered the right details!', 'danger')
            return redirect(url_for('.set_pay'))
    return render_template("user_pay_set.html", title = 'Welcome Home',\
                                                                    form = form)

@owner_b.route('/confirm_pay_window/<email_id>/<pay>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def confirm_pay_window(email_id, pay):
    form = EmployeePaySetConfirmation()
    if form.validate_on_submit():
        if form.edit.data:
            return redirect(url_for('.set_pay'))
        else:
            return redirect(url_for('.employee_set_pay', email_id = email_id,\
                                                                    pay = pay))
    return render_template('review_pay.html', form = form, amount = pay, \
                                            email_id = email_id, action = 'pay')

@owner_b.route('/employee_set_pay/<email_id>/<pay>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def employee_set_pay(email_id, pay):
    current_user = load_user(flask_login.current_user.id)
    if current_user.set_employee_pay(email_id, pay):
        flash('Pay entered successfully!', 'success')
    else:
        flash('Pay entered unsuccessfully!', 'danger')
    return render_template("owner_home.html", title = 'Welcome Home')

@owner_b.route('/upload_payslips', methods = ['GET', 'POST'])
@decorator_func
@owner_required
@login_required
def upload_payslips():
    form = EmployeeUploadPaySlip()
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
@owner_required
@login_required
def increment_employee_pay():
    form = EmployeeIncrementPay()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('.confirm_pay_inc_window', \
                            email_id = form.email_id.data, inc = form.inc.data))
        else:
            flash(f'Make sure you entered the right details!', 'danger')
            return redirect(url_for('.increment_employee_pay'))
    else:
        return render_template("increment_pay.html", title = 'Welcome Home',\
                                                                    form = form)

@owner_b.route('/confirm_pay_inc_window/<email_id>/<inc>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def confirm_pay_inc_window(email_id, inc):
    form = EmployeePaySetConfirmation()
    if form.validate_on_submit():
        if form.edit.data:
            return redirect(url_for('.increment_employee_pay'))
        else:
            return redirect(url_for('.employee_set_inc', email_id = email_id,\
                                                                    inc = inc))
    return render_template('review_pay.html', form = form, amount = inc, \
                                    email_id = email_id, action = 'increment')

@owner_b.route('/employee_set_inc/<email_id>/<inc>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def employee_set_inc(email_id, inc):
    current_user = load_user(flask_login.current_user.id)
    if current_user.increment_pay(email_id, inc):
        flash('Pay incremented successfully!', 'success')
    else:
        flash('Pay incremented unsuccessfully!', 'danger')
    return render_template("owner_home.html", title = 'Welcome Home')

@owner_b.route('/decrement_employee_pay', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def decrement_employee_pay():
    form = EmployeeDecrementPay()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('.confirm_pay_dec_window', \
                            email_id = form.email_id.data, dec = form.dec.data))
        else:
            flash(f'Make sure you entered the right details!', 'danger')
            return redirect(url_for('.decrement_employee_pay'))
    else:
        return render_template("decrement_pay.html", title = 'Welcome Home',\
                                                                    form = form)

@owner_b.route('/confirm_pay_dec_window/<email_id>/<dec>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def confirm_pay_dec_window(email_id, dec):
    form = EmployeePaySetConfirmation()
    if form.validate_on_submit():
        if form.edit.data:
            return redirect(url_for('.decrement_employee_pay'))
        else:
            return redirect(url_for('.employee_set_dec', email_id = email_id,\
                                                                    dec = dec))
    return render_template('review_pay.html', form = form, amount = dec, \
                                    email_id = email_id, action = 'decrement')

@owner_b.route('/employee_set_dec/<email_id>/<dec>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def employee_set_dec(email_id, dec):
    current_user = load_user(flask_login.current_user.id)
    if current_user.decrement_pay(email_id, dec):
        flash('Pay decremented successfully!', 'success')
    else:
        flash('Pay decremented unsuccessfully!', 'danger')
    return render_template("owner_home.html", title = 'Welcome Home')

@owner_b.route('/set_hire_date', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def set_hire_date():
    form = EmployeeSetHireDate()
    current_user = load_user(flask_login.current_user.id)
    if request.method == 'POST':
        if form.validate_on_submit():
            print(type(form.hire_date.data))
            current_user.set_employee_hire_date(form.email_id.data,
                                                form.hire_date.data)
            return redirect(url_for('.home'))
        else:
            flash(f'Make sure you entered the right details!', 'danger')
            return redirect(url_for('.set_hire_date'))
    return render_template('set_hire_date.html', form = form)

@owner_b.route('/set_bonus', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def set_bonus():
    form = EmployeeBonusSet()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('.confirm_bonus_window', \
                            email_id = form.email_id.data, bonus = form.bonus.data))
        else:
            flash(f'Make sure you entered the right details!', 'danger')
            return redirect(url_for('.set_bonus'))
    return render_template("set_bonus.html", title = 'Welcome Home',\
                                                                    form = form)

@owner_b.route('/confirm_bonus_window/<email_id>/<bonus>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def confirm_bonus_window(email_id, bonus):
    form = EmployeePaySetConfirmation()
    if form.validate_on_submit():
        if form.edit.data:
            return redirect(url_for('.set_bonus'))
        else:
            return redirect(url_for('.employee_set_bonus', email_id = email_id,\
                                                                    bonus = bonus))
    return render_template('review_pay.html', form = form, amount = bonus, \
                                            email_id = email_id, action = 'bonus')

@owner_b.route('/employee_set_bonus/<email_id>/<bonus>', methods = ['POST', 'GET'])
@decorator_func
@owner_required
@login_required
def employee_set_bonus(email_id, bonus):
    current_user = load_user(flask_login.current_user.id)
    if current_user.set_employee_bonus(email_id, bonus):
        flash('bonus entered successfully!', 'success')
    else:
        flash('bonus entered unsuccessfully!', 'danger')
    return render_template("owner_home.html", title = 'Welcome Home')

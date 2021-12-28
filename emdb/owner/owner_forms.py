from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                                        IntegerField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import DateField,DateTimeField
from flask_wtf.file import FileField

class EmployeePaySet(FlaskForm):
    email_id = StringField('Enter Employee Email', validators=[DataRequired()])
    pay = IntegerField('Enter pay', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeUploadPaySlip(FlaskForm):
    email_id = StringField('Enter Employee Email', validators=[DataRequired()])
    pay_slip = FileField('Pay Slip', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeIncrementPay(FlaskForm):
    email_id = StringField('Enter Employee Email', validators=[DataRequired()])
    inc = IntegerField('Enter Increment in percentage!', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeDecrementPay(FlaskForm):
    email_id = StringField('Enter Employee Email', validators=[DataRequired()])
    dec = IntegerField('Enter Decrement in percentage!', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeePaySetConfirmation(FlaskForm):
    edit = SubmitField('Edit')
    confirm = SubmitField('Confirm')

class EmployeeSetHireDate(FlaskForm):
    email_id = StringField('Enter Employee Email', validators=[DataRequired()])
    hire_date = DateField('Hiring Date', format='%Y-%m-%d',
                                                    validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeBonusSet(FlaskForm):
    email_id = StringField('Enter Employee Email', validators=[DataRequired()])
    bonus = IntegerField('Enter Bonus!', validators=[DataRequired()])
    submit = SubmitField('Submit')

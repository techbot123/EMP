from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                                        IntegerField)
from flask_wtf.file import FileField

class EmployeePaySet(FlaskForm):
    email_id = StringField('Enter Employee Email')
    pay = IntegerField('Enter pay')
    submit = SubmitField('Submit')

class EmployeeUploadPaySlip(FlaskForm):
    email_id = StringField('Enter Employee Email')
    pay_slip = FileField('Pay Slip')
    submit = SubmitField('Submit')

class EmployeeIncrementPay(FlaskForm):
    email_id = StringField('Enter Employee Email')
    inc = IntegerField('Enter Increment in percentage!')
    submit = SubmitField('Submit')

class EmployeeDecrementPay(FlaskForm):
    email_id = StringField('Enter Employee Email')
    dec = IntegerField('Enter Decrement in percentage!')
    submit = SubmitField('Submit')

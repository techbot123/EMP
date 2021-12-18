from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField

class EmployeeEmailSearch(FlaskForm):
    email_id = StringField('Enter Email')
    pay = IntegerField('Enter pay')
    submit = SubmitField('Search')

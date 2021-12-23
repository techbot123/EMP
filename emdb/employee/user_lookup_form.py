from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from emdb import db

class UserLookupForm(FlaskForm):
    search_name = StringField('Enter Name')
    search = SubmitField('Search')

class ChangePersonalInfo(FlaskForm):
    address = SubmitField('Change your Address')
    phone = SubmitField('Change your Phone')
    email = SubmitField('Change your Email')
    profile_image = SubmitField('Change your Profile picture')

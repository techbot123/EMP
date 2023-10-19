from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from emdb import db
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class UserLookupForm(FlaskForm):
    search_name = StringField('Enter Name')
    search = SubmitField('Search')

class ChangePersonalInfo(FlaskForm):
    address = SubmitField('Change your Address')
    phone = SubmitField('Change your Phone')
    email = SubmitField('Change your Email')
    profile_image = SubmitField('Change your Profile picture')
    pay_slips = SubmitField('View your pay slips')

class SearchBox(FlaskForm):
    search_box = StringField('What are you looking for? :*')
    like = SubmitField('Like')
    dislike = SubmitField('Dislike')
    search = SubmitField('Search')

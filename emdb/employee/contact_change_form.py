from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                                        IntegerField, FileField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField,DateTimeField
import phonenumbers
# from emdb import db

class AddressChangeForm(FlaskForm):
    address_line_1 = StringField('Address Line 1',
                           validators=[DataRequired(), Length(min=2, max=50)])
    address_line_2 = StringField('Address Line 2',
                           validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('City',
                           validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State',
                           validators=[DataRequired(), Length(min=2, max=50)])
    zipcode = StringField('zipcode', validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Submit')

class EmailChangeForm(FlaskForm):
    email_id = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class PhoneChangeForm(FlaskForm):
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Submit')

class ProfileImageChange(FlaskForm):
    profile_image = FileField('Image')
    submit = SubmitField('Upload')

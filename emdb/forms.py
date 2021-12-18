from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField,DateTimeField
from flask_wtf.file import FileField
import phonenumbers
from emdb import db

class RegistrationForm(FlaskForm):
    first_name = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email_id = StringField('Email',
                        validators=[DataRequired(), Email()])
    address_line_1 = StringField('Address Line 1',
                           validators=[DataRequired(), Length(min=2, max=50)])
    address_line_2 = StringField('Address Line 2',
                           validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('City',
                           validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State',
                           validators=[DataRequired(), Length(min=2, max=50)])
    zipcode = StringField('zipcode', validators=[DataRequired(), Length(min=2, max=10)])
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=10, max=15)])
    birth_date = DateField('Date of birth', format='%Y-%m-%d', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message = 'Passwords must match!')])
    profile_image = FileField('Image')
    submit = SubmitField('Sign Up')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    email_id = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')

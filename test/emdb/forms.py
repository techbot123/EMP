from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField,DateTimeField
from flask_wtf.file import FileField
import phonenumbers
from emdb import db

class RegistrationForm(FlaskForm):
    first_name = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    gender = RadioField('Gender', choices=[(1, 'Male'), (0, 'Female'), (2, 'Other')], \
                                                    validators=[DataRequired()])
    looking_for = RadioField('Looking for', choices=[(1, 'Male'), (0, 'Female'),\
                                  (2, 'Not Sure')], validators=[DataRequired()])
    birth_date = DateField('Date of birth', format='%Y-%m-%d', validators=[DataRequired()])
    height = IntegerField('Enter Height in centimeters', validators = [DataRequired()])
    # age = IntegerField('Enter age', validators = [DataRequired()])
    smoke = RadioField('Do you smoke?', choices=[(1, 'Frequently'), \
                                                (2, 'socially'), (0, 'Never')])
    cannabis = RadioField('Cannabis', choices=[(1, 'Frequently'), \
                                                (2, 'socially'), (0, 'Never')])
    alcohol = RadioField('alcohol', choices=[(1, 'Frequently'), \
                                                (2, 'socially'), (0, 'Never')])
    ethnicity = RadioField('ethnicity', choices=[(1, 'Caucassian'), (2, 'Asian'),\
        (3, 'African'), (4, 'Indian'), (5, 'Other')],validators=[DataRequired()])
    pvt_message = StringField('About you.. this will be hidden and will not be displayed on your profile',
                           validators=[DataRequired(), Length(min=10, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message = 'Passwords must match!')])
    # profile_image = FileField('Image')
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

class UploadPhotosForm(FlaskForm):
    profile_image = FileField('Profile Image', validators=[DataRequired()])
    image1 = FileField('Image 1')
    image2 = FileField('Image 2')
    image3 = FileField('Image 3')
    image4 = FileField('Image 4')
    image5 = FileField('Image 5')
    submit = SubmitField('Upload')
    # profile_image = FileField('Image')

class PersonalUserInfo(FlaskForm):
    smoke = RadioField('Do you smoke?', choices=[(1, 'Frequently'), \
                                                (2, 'socially'), (0, 'Never')])
    cannabis = RadioField('Cannabis', choices=[(1, 'Frequently'), \
                                                (2, 'socially'), (0, 'Never')])
    alcohol = RadioField('alcohol', choices=[(1, 'Frequently'), \
                                                (2, 'socially'), (0, 'Never')])
    ethnicity = RadioField('ethnicity', choices=[(1, 'Caucassian'), (2, 'Asian'),\
        (3, 'African'), (4, 'Indian'), (5, 'Other')],validators=[DataRequired()])
    pvt_message = StringField('About you.. this will be hidden and will not be displayed on your profile',
                           validators=[DataRequired(), Length(min=10, max=50)])
    submit = SubmitField('Find me a match now!')

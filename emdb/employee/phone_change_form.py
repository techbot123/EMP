from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField,DateTimeField
import phonenumbers
# from emdb import db

class PhoneChangeForm(FlaskForm):
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField,DateTimeField
import phonenumbers

class EmailChangeForm(FlaskForm):
    email_id = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

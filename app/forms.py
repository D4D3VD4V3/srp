from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import Login 


class SignUpForm(FlaskForm):
#TODO Custom validator for the roll number that checks with the current year
    Roll_Number = StringField("Roll Number:", validators=[DataRequired('Please enter your roll number'),
                                                          Length(min=10, max=10, message="Please enter a roll number of valid length")])
    Email_Address1 = StringField("Email address", validators=[DataRequired("Please enter your email address"), Email(message="Please enter a valid email address")])
    Email_Address2 = StringField("Confirm email address", validators=[EqualTo("Email_Address1", message="Email addresses must match")])
    Password1 = PasswordField("Password", validators=[DataRequired('Please enter a password'), Length(min=8, max=256, message="Please enter a password between 8 and 256 characters inclusive")])
    Password2 = PasswordField("Confirm password", validators=[EqualTo("Password1", message="Passwords must match")])
    Submit = SubmitField("Submit")

    def validate_Roll_Number(self, field):
        if Login.query.filter_by(rollno=field.data).first() is not None:
            raise ValidationError("There is an account associated with that roll number")

    def validate_Email_Address1(self, field):
        if Login.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("There is an account associated with that email ID")


class LoginForm(FlaskForm):
    Email_Address = StringField("Email address", validators=[DataRequired("Please enter your email address"), Email(message="Please enter a valid email address")])
    Password = PasswordField("Password", validators=[DataRequired('Please enter a password'), Length(min=8, max=256, message="Please enter a password between 8 and 256 characters inclusive")])
    Submit = SubmitField("Submit")

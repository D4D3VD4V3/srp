from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignUpForm(FlaskForm):
#TODO Custom validator for the roll number that checks with the current year
#TODO Check if roll no or email id *already* exists in the DB
#TODO Cannot use Length() validator with IntegerField coz int has no len(). Find workaround
    Roll_Number = StringField("Roll Number:", validators=[DataRequired('Please enter your roll number'), Length(min=10, max=10, message="Please enter a roll number of valid length")])
    Email_Address1 = StringField("Email address", validators=[DataRequired("Please enter your email address"), Email(message="Please enter a valid email address")])
    Email_Address2 = StringField("Confirm email address", validators=[EqualTo("Email_Address1", message="Email addresses must match")])
    Password1 = PasswordField("Password", validators=[DataRequired('Please enter a password'), Length(min=8, max=256, message="Please enter a password between 8 and 256 characters inclusive")])
    Password2 = PasswordField("Confirm password", validators=[EqualTo("Password1", message="Passwords must match")])
    Submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    Email_Address = StringField("Email address", validators=[DataRequired("Please enter your email address"), Email(message="Please enter a valid email address")])
    Password = PasswordField("Password", validators=[DataRequired('Please enter a password'), Length(min=8, max=256, message="Please enter a password between 8 and 256 characters inclusive")])
    Submit = SubmitField("Submit")

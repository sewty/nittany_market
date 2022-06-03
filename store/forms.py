from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from store.models import User

class RegisterForm(FlaskForm):

    # is there already a user w/ the same email?
    def validate_email(self, check_email):
        email_addr = User.query.filter_by(email=check_email.data).first()
        if email_addr:
            raise ValidationError('Email address already exists! Please try another email')

    email = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email Address: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

# should add validation for old password != new password
class ChangePasswordForm(FlaskForm):
    password1 = PasswordField(label='Old Password: ', validators=[DataRequired()])
    password2 = PasswordField(label='New Password: ', validators=[Length(min=8), DataRequired()])
    password3 = PasswordField(label='Confirm New Password: ', validators=[EqualTo('password2'), DataRequired()])
    submit = SubmitField(label='Change Password')

# move category and seller validation to here
class ProductListingForm(FlaskForm):
    category = StringField(label='Product Category:', validators=[DataRequired()])
    title = StringField(label='Product Title:', validators=[DataRequired()])
    name = StringField(label='Product Name:', validators=[DataRequired()])
    desc = StringField(label='Product Description:', validators=[DataRequired()])
    price = StringField(label="Sell Price:", validators=[DataRequired()])
    quantity = IntegerField(label='Quantity:', validators=[DataRequired()])
    submit = SubmitField(label='Create Listing')
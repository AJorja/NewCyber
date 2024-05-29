from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, IntegerField, PasswordField, FileField
from flask_wtf.file import FileRequired
from models import User

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"class": "border border-primary rounded text-primary bg-light"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"class": "border border-primary rounded text-primary bg-light"})
    message = StringField("Message", validators=[DataRequired()], render_kw={"class": "border border-primary rounded text-primary bg-light"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary btn-block"})

class RegistrationForm(FlaskForm):
    email_address = StringField("Email Address (Username)", validators=[DataRequired(), Email()])
    name = StringField("Full Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email_address(self, email_address_to_register):
        user = User.query.filter_by(email_address=email_address_to_register.data).first()
        if user is not None:
            raise ValidationError("Please Use a Different Email Address)")
        
class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ResetPasswordForm(FlaskForm):
    new_password = StringField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
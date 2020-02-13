from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from .models import User
from flask import flash


#Login Form
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")

#Registration Form
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired("Email is required"),Email()]) #required field, checks if it is an Email
    username = StringField('Username',validators=[DataRequired('Username is required')])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        #check to see if that email has been activated/registered by querying User table
        if User.query.filter_by(email=field.data).first():
            #raise ValidationError('Your email has been already registered!')
            flash("Your email has been already registered!")

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            #raise ValidationError('Username is taken!')
            flash("Username is taken!")

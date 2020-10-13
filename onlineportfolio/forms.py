from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class AddCVForm(FlaskForm):
    cv_file = FileField('Add CV', validators=[
                        FileAllowed(['doc', 'docx', 'pdf'])])
    submit = SubmitField('Upload')


class AddAboutForm(FlaskForm):
    self_desc = StringField('About', validators=[
                            DataRequired()])
    submit = SubmitField('Save')


class DownloadCVForm(FlaskForm):
    cvsubmit = SubmitField('Download CV')


class EmailForm(FlaskForm):
    fname = StringField('First Name', validators=[
                        DataRequired(), Length(min=2, max=30)])
    lname = StringField('Last Name', validators=[
                        DataRequired(), Length(min=2, max=30)])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Your Message', validators=[
                            DataRequired(), Length(min=2)])
    emailsubmit = SubmitField('Send Message')

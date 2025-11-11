from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length
from wtforms import RadioField, SubmitField,StringField, PasswordField, SelectField, RadioField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired
from wtforms import FileField


# Registration form for user registration
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=6, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=150)])
    role = SelectField('Role', choices=[('Annotator', 'Annotator'), ('Developer', 'Developer')], default='Annotator')

# Login form for user login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class AnnotationForm(FlaskForm):
    annotation = RadioField('Annotation', choices=[
        ('Privacy-Related Feature Request', 'Privacy-Related Feature Request'),
        ('Privacy-Related Bug', 'Privacy-Related Bug'),
        ('Privacy-Related Feature Request+Bug', 'Privacy-Related Feature Request+Bug'),
        ('Not Privacy-Related', 'Not Privacy-Related')
    ])
    submit = SubmitField('Submit')

class ScrapeReviewsForm(FlaskForm):
    app_id = StringField('App ID', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    count = IntegerField('Review Count')
    submit = SubmitField('Scrape')
# OTP form for OTP verification during registration
class OTPForm(FlaskForm):
    otp = StringField('OTP', validators=[InputRequired()])
class UploadCSVForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Upload')
class InviteAnnotatorsForm(FlaskForm):
    invited_annotators_emails = StringField('Emails', validators=[DataRequired()])
    submit = SubmitField('Invite')
class ReviewFeedbackForm(FlaskForm):
    # no fields needed—just CSRF
    pass
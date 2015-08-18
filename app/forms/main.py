from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, DateField, SelectField
from wtforms.validators import Required, Length, Email, EqualTo, DataRequired, AnyOf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.forms.widgets import SelectDateWidget, ButtonGroupWidget


class LoginForm(Form):
    email       = TextField('E-Mail Address',    validators=[Length(max=120)],
                                                 description={'placeholder':"E-Mail"})
    password    = PasswordField('Password',      description={'placeholder':"Password"})
    remember_me = BooleanField('remember_me',    default = False)


class SignupForm(Form):
    givenname   = TextField('First Name',        validators=[Required(), Length(max=30)])
    surname     = TextField('Last Name',         validators=[Required(), Length(max=30)])
    email       = TextField('E-Mail Address',    validators=[Required(), Length(max=120), Email()],
                                                 description={'help': "You will use this email address to log into your account.",
                                                              'placeholder':"Enter email"})
    password    = PasswordField('Password',      validators=[Required(), 
                                                             Length(min=6, max=20),
                                                             EqualTo('confirm', message="Passwords must match")],
                                                 description={'placeholder': "Password"})
    confirm     = PasswordField('Verify Password', description={'placeholder': "Repeat your password"})
    accept_tos  = BooleanField('Accept TOS',    validators=[Required()],
                                                description={'help': "Agree to the Terms of Service"})
    invite_code = TextField('Invitation Code',  validators=[Required(), AnyOf(['AskMeAboutAnime'], 'Invalid Invitation Code')],
                                                description={'help': 'Registrations are currently invite only.'} )



class QuestionForm(Form):
    title    = TextField('Title / Short Description', validators=[Required(), Length(max=50)],
                                    description={'placeholder': 'Question Title'})
    category = TextField('Category', validators=[Required(), Length(max=50)],
                                    description={'placeholder': 'Category Name'})


SLIDE_TYPES = [
    ('title',   'Title'),
    ('text',    'Text'),
    ('choice',  'Multiple Choice'),
    ('video',   'Video')
]

class SlideForm(Form):
    slide_type  = SelectField('Slide Type', choices=SLIDE_TYPES, validators=[DataRequired()])
    prompt      = TextField('Prompt Text', validators=[Length(max=1000)])
    
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    text = StringField("Message", validators=[DataRequired()], render_kw={'autofocus': True})
    to = StringField("To", validators=[DataRequired()])
    submit = SubmitField("Send")


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username")
    challenge = PasswordField("Challenge")
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Save")

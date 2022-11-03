from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    who = StringField("Who", validators=[DataRequired()])
    to = StringField("To", validators=[DataRequired()])
    text = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    challenge = PasswordField("Challenge")
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Save")

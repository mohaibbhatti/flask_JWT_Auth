from flask_wtf import FlaskForm
from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(3222), nullable=False)
    reset_token = db.Column(db.String(255), unique=True, nullable=True)


    def __repr__(self):
        return f'<User {self.username}>'
    

    def __init__(self, username, password):
        self.username = username
        self.password = password

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

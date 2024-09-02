from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(60), unique=True, nullable=False)
    password = db.Column(String(128), nullable=False)
    user_jwt = 

    def __init__(self, name, password):
        self.name = name
        self.password = password

from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registerTime = db.Column(db.DateTime(timezone=True), nullable=False)

def __init__(self, username, email, password, created) :
        self.username = username
        self.email = email
        self.password = bcrypt.encrypt(password)
        self.registerTime = registerTime

#to validate the encrypted password
def validate_password(self, password):
        return bcrypt.verify(password, self.password)

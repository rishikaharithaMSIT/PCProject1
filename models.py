from flask_sqlalchemy import SQLAlchemy

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
        self.password = password
        self.registerTime = registerTime

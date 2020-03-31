from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registerTime = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, email, password, created):
        self.email = email
        self.password = password
        self.registerTime = registerTime

class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, isbn, title, author, year) :
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        

"""
This file is to render the book details

"""
from models import db, Books

def get_book_details(isbn):
    book = Books.query.get(isbn)
    if book is None:
        return None
    return book
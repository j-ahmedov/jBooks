from base64 import b64encode
from jbook_app.models import *
from flask import Flask, send_file, session
from datetime import timedelta, datetime
from io import BytesIO
from flask_mail import Mail, Message


my_app = Flask(__name__)
my_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myp0stgr3sql@localhost/jBooksDB'
my_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
my_app.config['SECRET_KEY'] = '123456789zxc'
my_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

my_app.config['MAIL_SERVER']='smtp.gmail.com'
my_app.config['MAIL_PORT'] = 587
my_app.config['MAIL_USERNAME'] = 'j.ahmedov.m99@gmail.com'
my_app.config['MAIL_PASSWORD'] = '1sforchann3ls2019'
my_app.config['MAIL_USE_TLS'] = True
my_app.config['MAIL_USE_SSL'] = False

mail = Mail(my_app)

db.init_app(my_app)


# ----------------------------------Functions------------------------------------------------
# Function to check if admin username and password already exist
def checkAdmin(_username, _password):
    adminResult = db.session.query(Admin).filter(
        Admin.username == _username,
        Admin.password == _password
    )

    for result in adminResult:
        if result is not None:
            if result.username == _username and result.password == _password:
                session.permanent = True
                session['loggedin'] = True
                session['username'] = _username
                return True

    return False

# ---------------------------------------------------------------
# Function to check if the book data already exists 
def checkBook(_bookTitle, _bookAuthor):
    bookResult = db.session.query(Book).filter(
        Book.title == _bookTitle,
        Book.author == _bookAuthor
    )

    for result in bookResult:
        if result is not None:
            if result.title == _bookTitle and result.author == _bookAuthor:
                return True
    return False

# ---------------------------------------------------------------------------
# Function to add book data to Database
def addBook(_book): 
    try:
        db.session.add(_book)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

# ---------------------------------------------------------
# Function, that returns all book data from database
def getAllBook():
    return Book.query.all()

# ----------------------------------------------------------
# Function, that returns all books for users
def getAllBooksForUsers():
    bookList = []
    _books = Book.query.order_by(Book.id.desc()).all()
    for i in _books:
        bookDict = {
            'id': i.id,
            'title': i.title,
            'author': i.author,
            'description': i.description,
            'img': b64encode(i.img_data).decode()
            },
        bookList.append(bookDict)
    return bookList


# -------------------------------------------------------
# Function to return book by Category
def getBookByCategory(_category):
    bookList = []
    _books = Book.query.filter_by(category=_category).all()
    for i in _books:
        bookDict = {
            'id': i.id,
            'title': i.title,
            'author': i.author,
            'description': i.description,
            'img': b64encode(i.img_data).decode()
            },
        bookList.append(bookDict)
    return bookList


# -------------------------------------------------------
# Function to get book by searching
def getBookBySearch(_searchWord):
    _searchWord1 = _searchWord.lower()
    _searchWord2 = _searchWord.title()
    bookList = []
    _books = Book.query.filter(Book.title.contains(_searchWord1) | Book.title.contains(_searchWord2) |
    Book.description.contains(_searchWord1) | Book.description.contains(_searchWord2)).all()
    for i in _books:
        bookDict = {
            'id': i.id,
            'title': i.title,
            'author': i.author,
            'description': i.description,
            'img': b64encode(i.img_data).decode()
            },
        bookList.append(bookDict)
    return bookList


# -------------------------------------------------------
# Function to delete book by ID
def deleteBookById(book_id):
    Book.query.filter_by(id=book_id).delete()
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True


# ------------------------------------------------------
# Function to update book data on database
def updateBook(_updated_book):
    book = Book.query.filter_by(id=_updated_book['book_id']).first()
    if book is not None:
        Book.query.filter_by(id=_updated_book['book_id']).update(
            {
                'title': _updated_book['book_title'],
                'author': _updated_book['book_author'],
                'description': _updated_book['book_description'],
                'category': _updated_book['book_category'],
                'img_name': _updated_book['book_img'].filename,
                'img_data': _updated_book['book_img'].read(),
                'file_name': _updated_book['book_file'].filename,
                'file_data': _updated_book['book_file'].read(),
                'admin': _updated_book['admin_name']
            }
        )

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True
    return False

# ----------------------------------------------------
# Function to download book image from database
@my_app.route('/download-img/<book_id>')
def download_img(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return send_file(BytesIO(book.img_data), attachment_filename=book.img_name, as_attachment=True)


# ----------------------------------------------------
# Function to download book file from database
@my_app.route('/download-file/<book_id>')
def download_file(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return send_file(BytesIO(book.file_data), attachment_filename=book.file_name, as_attachment=True)


# --------------------------------------------------------------
# Function to send message from users to moderators
def send_mail(_senderName, _senderEmail, _senderMessage):
    msg = Message(
        f'Message from {_senderName}',
        sender=_senderEmail,
        recipients=['j.ahmedov.m99@gmail.com']
    )
    msg.body = f'{_senderMessage}\n\nWhith regard!\n{_senderEmail}'

    try:
        mail.send(msg)
    except Exception as e:
        print(e)
        return False
    return True
    


from jbook_app import views
from jbook_app import admin_views

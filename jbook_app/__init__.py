from multiprocessing import AuthenticationError
from datetime import datetime
from flask import Flask, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


my_app = Flask(__name__)
my_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myp0stgr3sql@localhost/jBooksDB'
my_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
my_app.config['SECRET_KEY'] = '123456789zxc'
my_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(my_app)


# -------------------------Models--------------------------------------
# Model Admin
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __init__(self, username, password):
        self.username = username
        self.password = password

# ----------------------------------------------------
# Model Book
class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    description = db.Column(db.String(200))
    category = db.Column(db.String(50))
    img_name = db.Column(db.String(50))
    img_data = db.Column(db.LargeBinary)
    file_name = db.Column(db.String(50))
    file_data = db.Column(db.LargeBinary)
    added_date = db.Column(db.Date)
    admin = db.Column(db.String(30))

    def __init__(self, title, author, description, category, img_name, img_data,
                        file_name, file_data, added_date, admin):
        self.title = title
        self.author = author
        self.description = description
        self.category = category
        self.img_name = img_name
        self.img_data = img_data
        self.file_name = file_name
        self.file_data = file_data
        self.added_date = added_date
        self.admin = admin

 # ------------------------------------------------------------------------------------------


# ----------------------------------Functions------------------------------------------------
# Function to check admin username and password already exist
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
# Function to check wether the book data already exists 
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
def bookAdd(_bookTitle, _bookAuthor, _bookDescription, _bookCategory, _bookImage, _bookFile, _admin):

    book = Book(
        title=_bookTitle,
        author=_bookAuthor,
        description=_bookDescription,
        category=_bookCategory,
        img_name=_bookImage.filename,
        img_data=_bookImage.read(),
        file_name=_bookFile.filename,
        file_data=_bookFile.read(),
        added_date=datetime.now().date(),
        admin=_admin)

    try:
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

# ---------------------------------------------------------
# Function, that returns all book data from database
def getAllBook():
    return Book.query.all()


from jbook_app import views
from jbook_app import admin_views

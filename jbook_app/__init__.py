from flask import Flask, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


my_app = Flask(__name__)
my_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myp0stgr3sql@localhost/jBooksDB'
my_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
my_app.config['SECRET_KEY'] = '123456789zxc'
my_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(my_app)


# Model Admin
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __init__(self, username, password):
        self.username = username
        self.password = password


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
    

# Function to check admin username and password
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


from jbook_app import views
from jbook_app import admin_views

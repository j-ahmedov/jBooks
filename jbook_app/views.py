from jbook_app import getAllBook, getAllBooksForUsers, my_app
from flask import render_template

# For users
@my_app.route('/')
def main_page():
    _books = getAllBooksForUsers()
    return render_template('for_users/home.html', books=_books)


@my_app.route('/about')
def about_page():
    return render_template('for_users/about.html')


@my_app.route('/contact')
def contacts_page():
    return render_template('for_users/contact.html')

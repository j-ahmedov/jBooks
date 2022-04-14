from jbook_app import getAllBook, my_app, checkAdmin, checkBook, bookAdd, getBookById
from flask import render_template, redirect, request, session, url_for, flash

    
def handleFormData():
    book_title = request.form.get("book_title")
    book_author = request.form.get("book_author")
    book_description = request.form.get("book_description")
    book_category = request.form.get("book_category")
    book_img = request.files['book_img']
    book_file = request.files['book_file']
    admin_name = session['username']

    if checkBook(book_title, book_author):
        # flash(f'The book already exists! <br/>Title: {book_title} <br/>Author: {book_author}')
        return redirect(url_for('admin_work'))
    
    if bookAdd(book_title, book_author, book_description, book_category, book_img, book_file, admin_name):
        return redirect(url_for('admin_work'))
    else:
        # flash('Cannot upload book data to database')
        return redirect(url_for('admin_work'))


# These are for admin pages
@my_app.route('/admin', methods=["POST", "GET"])
def my_admin():
    if 'loggedin' in session:
        return redirect(url_for('admin_work'))
    else:
        if request.method == "POST":
            admin_username = request.form.get("admin_username")
            admin_password = request.form.get("admin_password")
            if checkAdmin(admin_username, admin_password):
                return redirect(url_for('admin_work'))
            else:
                flash("Incorrect username or password !")
                return redirect(url_for('my_admin'))
        
        return render_template('for_admin/admin_login.html')


@my_app.route('/admin-work', methods=["POST", "GET"])
def admin_work():
    if 'loggedin' in session:
        if request.method == "GET":
            admin_name = session['username']
            _books = getAllBook()
            return render_template('for_admin/admin_workspace.html', admin_name=admin_name, books=_books)
        elif request.method == "POST":
            print(request.form.get('bookId'))
            return redirect(url_for('admin_work'))
        
            
    else:
        return redirect(url_for('my_admin'))
 

@my_app.route('/admin/add-book', methods=["POST", "GET"])
def addBook():
    if 'loggedin' in session:
        # if request.method == "POST":
        #     handleFormData()
        return render_template('for_admin/admin_book.html', formTitle='Add Book')
    else:
        return redirect(url_for('my_admin'))


# @my_app.route('/admin/edit-book/<int:book_id>', methods=["POST", "GET"])
# def editBook(book_id):
#     if 'loggedin' in session:
#         bookDict = getBookById(book_id)
#         # if request.method == "POST":
#         #     handleFormData()
#         return render_template('for_admin/admin_book.html', formTitle='Edit Book')
#     else:
#         return redirect(url_for('my_admin'))


@my_app.route('/admin-logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('my_admin'))

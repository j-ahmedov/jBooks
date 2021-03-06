from jbook_app import deleteBookById, getAllBook, my_app, checkAdmin, checkBook, addBook, updateBook
from flask import render_template, redirect, request, session, url_for, flash
from jbook_app.models import Book
from datetime import timedelta, datetime

# ----------------------- Admin page routes -------------------------------------
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


# ------------------------------------------------------------------
# Admin workspace route
@my_app.route('/admin-work', methods=["POST", "GET"])
def admin_work():
    if 'loggedin' in session:
        if request.method == "GET":
            admin_name = session['username']
            _books = getAllBook()
            return render_template('for_admin/admin_workspace.html', admin_name=admin_name, books=_books)
        elif request.method == "POST":
            if handleToUpdate():
                flash('The book has been successfully updated')
                return redirect(url_for('admin_work'))
            else:
                flash('Cannot update book')
                return redirect(url_for('admin_work'))
    else:
        return redirect(url_for('my_admin'))
 

# ------------------------------------------------------------------
# Add book route
@my_app.route('/admin/add-book', methods=["POST", "GET"])
def add_book():
    if 'loggedin' in session:
        if request.method == "POST":
            if bookExists():
                flash('The book already exists!')
                return redirect(url_for('add_book'))

            if handleToAdd():
                flash('The book has been successfully added')
                return redirect(url_for('admin_work'))
            else:
                flash('Cannot upload book to database')
                return redirect(url_for('admin_work'))
        return render_template('for_admin/admin_book.html')
    else:
        return redirect(url_for('my_admin'))


# ------------------------------------------------------------------
# Delete book route
@my_app.route('/admin/delete-book/<int:book_id>', methods=["POST", "GET"])
def delete_book(book_id):
    if 'loggedin' in session:
        if deleteBookById(book_id):
            flash('Book has been successfully deleted')
            return redirect(url_for('admin_work'))
        else:
            flash('Cannot delete this book')
            return redirect(url_for('admin_work'))
    else:
        return redirect(url_for('my_admin'))


# ------------------------------------------------------------------
# Admin logout route
@my_app.route('/admin-logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('my_admin'))


# ------------------------------------------------------------------
# Function to add book data to database 
def bookExists():
    book_title = request.form.get("book_title")
    book_author = request.form.get("book_author")
    if checkBook(book_title, book_author):
        return True
    return False


# ------------------------------------------------------------------
# Function to add book data to database    
def handleToAdd():
    book_title = request.form.get("book_title")
    book_author = request.form.get("book_author")
    book_description = request.form.get("book_description")
    book_category = request.form.get("book_category")
    book_img = request.files['book_img']
    book_file = request.files['book_file']
    admin_name = session['username']
    
    book = Book(
        title=book_title,
        author=book_author,
        description=book_description,
        category=book_category,
        img_name=book_img.filename,
        img_data=book_img.read(),
        file_name=book_file.filename,
        file_data=book_file.read(),
        added_date=datetime.now().date(),
        admin=admin_name)

    if addBook(book):
        return True
    else:
        return False


# ------------------------------------------------------------------
# Function to handle form values to update data on database
def handleToUpdate():
    book_id = request.form.get('book_id')
    book_title = request.form.get("book_title")
    book_author = request.form.get("book_author")
    book_description = request.form.get("book_description")
    book_category = request.form.get("book_category")
    book_img = request.files['book_img']
    book_file = request.files['book_file']
    admin_name = session['username']
    
    updated_book = {
        'book_id': book_id,
        'book_title': book_title,
        'book_author': book_author,
        'book_description': book_description,
        'book_category': book_category,
        'book_img': book_img,
        'book_file': book_file,
        'admin_name': admin_name
    }

    if updateBook(updated_book):
        return True
        
    else:
        return False
       
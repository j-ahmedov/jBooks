from jbook_app import getAllBooksForUsers, getBookByCategory, my_app, send_mail
from flask import flash, redirect, render_template, request, url_for


# For users
@my_app.route('/')
def main_page():
    _books = getAllBooksForUsers()
    _book_type = 'Latest'
    return render_template('for_users/home.html', books=_books, book_type=_book_type)


@my_app.route('/category/<category_num>')
def science_category(category_num):
    categoryDict = {
        '1' : 'Science', 
        '2' : 'Literature', 
        '3' : 'Language', 
        '4' : 'Business', 
        '5' : 'Programming', 
        '6' : 'Self development', 
    }
    _books = getBookByCategory(categoryDict[category_num])
    _book_type = categoryDict[category_num]
    return render_template('for_users/home.html', books=_books, book_type=_book_type)


@my_app.route('/about')
def about_page():
    return render_template('for_users/about.html')


@my_app.route('/contact', methods=['POST', 'GET'])
def contact_page():
    if request.method == 'POST':
        sender_name = request.form['sender_name']
        sender_email = request.form['sender_email']
        sender_message = request.form['sender_message']
        if send_mail(sender_name, sender_email, sender_message):
            flash('The message has been successfully sent')
            return redirect(url_for('contact_page'))
        else:
            flash('Something went wrong')
            return redirect(url_for('contact_page'))
    return render_template('for_users/contact.html')

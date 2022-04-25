from jbook_app import getAllBooksForUsers, getBookByCategory, getBookBySearch, my_app, send_mail
from flask import flash, redirect, render_template, request, url_for


# ---------------------------For users-------------------------------------------------
# Main route
@my_app.route('/', methods=['POST', 'GET'])
def main_page():
    search_word = request.args.get('search_word')
    if search_word:
        _books = getBookBySearch(search_word)
        _bookType = 'Searched'
    else:
        _books = getAllBooksForUsers()
        _bookType = 'Latest'
    return render_template('for_users/home.html', books=_books, book_type=_bookType)


# -------------------------------------------------------------------------------
# Category routes
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


# -------------------------------------------------------------------------------
# About route
@my_app.route('/about')
def about_page():
    return render_template('for_users/about.html')


# -------------------------------------------------------------------------------
# Contact us route
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


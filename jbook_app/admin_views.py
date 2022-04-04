from jbook_app import my_app, checkAdmin
from flask import render_template, redirect, request, session, url_for, flash


ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXTENSION = 'pdf'


def allowed_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == ALLOWED_EXTENSION


def getFormValues():
    value_list = []
    value_list.append(request.form.get("book_title"))
    value_list.append(request.form.get("book_author"))
    value_list.append(request.form.get("book_description"))
    value_list.append(request.form.get("book_category"))
    value_list.append(request.form.get("book_img"))
    value_list.append(request.form.get("book_file"))
    return value_list


def checkInputFilled(_valueList):

    for i in _valueList:
        if not i:
            return False
    return True




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
                redirect(url_for('my_admin'))
        
        return render_template('for_admin/admin_login.html')


@my_app.route('/admin-work', methods=["POST", "GET"])
def admin_work():
    if 'loggedin' in session:
        admin_name = session['username']
        return render_template('for_admin/admin_workspace.html', admin_name=admin_name)
    else:
        return redirect(url_for('my_admin'))


@my_app.route('/admin-book', methods=["POST", "GET"])
def admin_book():
    if 'loggedin' in session:
        if request.method == "POST":
            _valueList = getFormValues()
            if checkInputFilled(_valueList):
                flash("Everything is OK")
                return redirect(url_for('admin_book'))
            else:
                flash("All fields should be filled")
                return redirect(url_for('admin_book'))
        return render_template('for_admin/admin_book.html')
    else:
        return redirect(url_for('my_admin'))


@my_app.route('/admin-logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('my_admin'))

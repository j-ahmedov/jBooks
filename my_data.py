from flask import session

def checkToLogin(username, password):
    admin = True
    if admin:
        session.permanent = True
        session['loggedin'] = True
        return True
    else:
        return False

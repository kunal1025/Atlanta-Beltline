import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import db
import register

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = db.get_connection()
        error = None
        sql = 'select user.username, password from user join email where email = %s'
        with conn.cursor() as cursor:
            cursor.execute(sql, email)
            user = cursor.fetchone()
        if user is None:
            error = 'Incorrect email'
        elif not password == user['password']:
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['username'] = user['username']
            session['role'] = getRole(user['username'])
            print(session['role'])
            return redirect('/')

        flash(error)

    return render_template('auth/login.html')

def getRole(username):
    conn = db.get_connection()
    adminSql = 'select username from administrator where username = %s'
    managerSql = 'select username from manager where username = %s'
    staffSql = 'select username from staff where username = %s'
    visitorSql = 'select username from visitor where username = %s'
    admin = None
    manager = None
    staff = None
    visitor = None
    try:
        with conn.cursor() as cursor:
            cursor.execute(adminSql, username)
            admin = cursor.fetchone()
            cursor.execute(managerSql, username)
            manager = cursor.fetchone()
            cursor.execute(staffSql, username)
            staff = cursor.fetchone()
            cursor.execute(visitorSql, username)
            visitor = cursor.fetchone()
    except Exception as e:
        print(e)
        raise e
    if (admin):
        if (visitor):
            return 'admin-visitor'
        else:
            return 'admin'
    elif (manager):
        if (visitor):
            return 'manager-visitor'
        else:
            return 'manager'
    elif (staff):
        if (visitor):
            return 'staff-visitor'
        else:
            return 'staff'
    elif visitor:
        return 'visitor'
    else:
        return 'user'

@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect('/')
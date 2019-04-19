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
            return redirect('/transit')

        flash(error)

    return render_template('auth/login.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.get_connection()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        """elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {0} is already registered.'.format(username)
        
        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        """
        flash(error)

    return render_template('auth/register.html')
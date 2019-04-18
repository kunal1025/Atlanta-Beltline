import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import db

bp = Blueprint('register', __name__, url_prefix='/register')

@app.route('/user', methods=['GET', 'POST'])
    def register_user():
        if request.method == 'GET':
            return render_template('/auth/register_user.html')
        else:
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            username = request.form.get('username')
            password = request.form.get('password')
            emails = request.form.getlist('email[]')

            hashed_password = generate_password_hash(password)

            conn = db.get_connection()
            try:
                with conn.cursor() as cursor:
                    insertUser = 'INSERT INTO beltline.user (%s, %s, ‘Pending’, %s, %s)'
                    insertEmail = 'INSERT INTO beltline.email (%s, %s)'
                    cursor.execute(insertUser, (username, hashed_password, first_name, last_name))
                    cursor.commit()
                    for email in emails:
                        cursor.execute(insertEmail, (username, email))
                    cursor.commit()
            except Exception as e:
                print(e)
                // return render_template('/error/500.html')


            return redirect('/login')

@app.route('/visitor', methods=['GET', 'POST'])
    def register_visitor():
        if request.method == 'GET':
            return render_template('/auth/register_visitor.html')
        else:
            return redirect('/login')

@app.route('/employee', methods=['GET', 'POST'])
    def register_employee():
        if request.method == 'GET':
            return render_template('/auth/register_employee.html')
        else:
            return redirect('/login')

@app.route('/employee-visitor', methods=['GET', 'POST'])
    def register_employee_visitor():
        if request.method == 'GET':
            return render_template('/auth/register_employee-visitor.html')
        else:
            return redirect('/login')
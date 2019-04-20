# -*- coding: utf-8 -*-

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import db

bp = Blueprint('register', __name__, url_prefix='/auth/register')

@bp.route('/nav', methods=['GET'])
def register_navigation():
    return render_template('/functionality/register.html')

@bp.route('/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('/register/manage/register_user.html')
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
                insertVisitor = 'INSERT INTO beltline.visitor (%s)'
                insertEmail = 'INSERT INTO beltline.email (%s, %s)'
                cursor.execute(insertUser, (username, hashed_password, first_name, last_name))
                conn.commit()
                cursor.execute(insertVisitor, (username))
                conn.commit()
                for email in emails:
                    cursor.execute(insertEmail, (username, email))
                cursor.commit()
        except Exception as e:
            print(e)
            #return render_template('/error/500.html')
            return redirect('/register/user')


        return redirect('/login')

@bp.route('/visitor', methods=['GET', 'POST'])
def register_visitor():
    if request.method == 'GET':
        return render_template('/register/manage/register_visitor.html')
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
                insertVisitor = 'INSERT INTO beltline.visitor (%s)'
                insertEmail = 'INSERT INTO beltline.email (%s, %s)'
                cursor.execute(insertUser, (username, hashed_password, first_name, last_name))
                conn.commit()
                cursor.execute(insertVisitor, username)
                conn.commit()
                for email in emails:
                    cursor.execute(insertEmail, (username, email))
                cursor.commit()
        except Exception as e:
            print(e)
            #return render_template('/error/500.html')
            return redirect('/register/visitor')


        return redirect('/login')

@bp.route('/employee', methods=['GET', 'POST'])
def register_employee():
    if request.method == 'GET':
        return render_template('/auth/register_employee.html')
    else:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password = request.form.get('password')
        emails = request.form.getlist('email[]')
        usertype = request.form.get('type')
        employeeID = request.form.get('employeeID')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        hashed_password = generate_password_hash(password)

        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                insertUser = 'INSERT INTO beltline.user (%s, %s, ‘Pending’, %s, %s)'
                insertEmail = 'INSERT INTO beltline.email (%s, %s)'
                insertEmployee = 'INSERT INTO beltline.employee (%s, %s, %s, %s, %s, %s, %s)'
                if usertype == 'manager':
                    insertManager = 'INSERT INTO beltline.manager (%s)'
                else:
                    insertStaff = 'INSERT INTO beltline.staff (%s)'
                cursor.execute(insertUser, (username, hashed_password, first_name, last_name))
                conn.commit()
                cursor.execute(insertEmployee, (username, employeeID, phone, address, city, state, zipcode))
                conn.commit()
                cursor.execute(insertManager, (username))
                conn.commit()
                cursor.execute(insertStaff, (username))
                conn.commit()
                for email in emails:
                    cursor.execute(insertEmail, (username, email))
                cursor.commit()
        except Exception as e:
            print(e)
            #return render_template('/error/500.html')
            return redirect('/register/visitor')

        return redirect('/login')

@bp.route('/employee-visitor', methods=['GET', 'POST'])
def register_employee_visitor():
    if request.method == 'GET':
        return render_template('/auth/register_employee.html')
    else:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password = request.form.get('password')
        emails = request.form.getlist('email[]')
        usertype = request.form.get('type')
        employeeID = request.form.get('employeeID')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        hashed_password = generate_password_hash(password)

        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                insertUser = 'INSERT INTO beltline.user (%s, %s, ‘Pending’, %s, %s)'
                insertVisitor = 'INSERT Into beltline.visitor (%s)'
                insertEmail = 'INSERT INTO beltline.email (%s, %s)'
                insertEmployee = 'INSERT INTO beltline.employee (%s, %s, %s, %s, %s, %s, %s)'
                if usertype == 'manager':
                    insertManager = 'INSERT INTO beltline.manager (%s)'
                else:
                    insertStaff = 'INSERT INTO beltline.staff (%s)'
                cursor.execute(insertUser, (username, hashed_password, first_name, last_name))
                conn.commit()
                cursor.execute(insertEmployee, (username, employeeID, phone, address, city, state, zipcode))
                conn.commit()
                cursor.execute(insertManager, (username))
                conn.commit()
                cursor.execute(insertStaff, (username))
                conn.commit()
                cursor.execute(insertVisitor, username)
                conn.commit()
                for email in emails:
                    cursor.execute(insertEmail, (username, email))
                conn.commit()
        except Exception as e:
            print(e)
            #return render_template('/error/500.html')
            return redirect('/register/visitor')

        return redirect('/login')

# -*- coding: utf-8 -*-

import functools
from random import randint
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import db

bp = Blueprint('register', __name__, url_prefix='/auth/register')

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@bp.route('/nav', methods=['GET'])
def register_navigation():
    return render_template('/functionality/register.html')

@bp.route('/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('/register/register_user.html')
    else:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password = request.form.get('password')
        emails = request.form.getlist('email[]')

        error = None
        conn = db.get_connection()
        with conn.cursor() as cursor:
            user = 'select username from user where username = %s'
            cursor.execute(user, (username))
            result1 = cursor.fetchone()

            invalidEmail = False
            for eachEmail in emails:
                email = 'select email from email where email = %s'
                cursor.execute(email, (eachEmail))
                result = cursor.fetchone()
                if (result):
                    invalidEmail = True

            if (result1 or invalidEmail):
                print("you dumb")
                return redirect('/')
            else:
                hashed_password = generate_password_hash(password)


                try:
                    with conn.cursor() as cursor:
                        insertUser = 'INSERT INTO beltline.user values (%s, %s, %s, %s, %s)'
                        pending = 'Pending'
                        insertEmail = 'INSERT INTO beltline.email values (%s, %s)'
                        cursor.execute(insertUser, (username, hashed_password, pending, first_name, last_name))
                        conn.commit()
                        for email in emails:
                            cursor.execute(insertEmail, (username, email))
                        conn.commit()
                except Exception as e:
                    print(e)
                    #return render_template('/error/500.html')
                    return redirect('/auth/login')


        return redirect('/auth/login')

@bp.route('/visitor', methods=['GET', 'POST'])
def register_visitor():
    if request.method == 'GET':
        return render_template('/register/register_visitor.html')
    else:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password = request.form.get('password')
        emails = request.form.getlist('email[]')

        hashed_password = generate_password_hash(password)

        conn = db.get_connection()
        with conn.cursor() as cursor:
            user = 'select username from user where username = %s'
            visitor = 'select username from visitor where username = %s'
            cursor.execute(user, (username))
            result1 = cursor.fetchone()
            cursor.execute(visitor, (username))
            result2 = cursor.fetchone()

            invalidEmail = False
            for eachEmail in emails:
                email = 'select email from email where email = %s'
                cursor.execute(email, (eachEmail))
                result = cursor.fetchone()
                if (result):
                    invalidEmail = True

            if (result1 or result2 or invalidEmail):
                print("you dumb")
                return redirect('/')
            else:
                try:
                    with conn.cursor() as cursor:
                        insertUser = 'INSERT INTO beltline.user values (%s, %s, %s, %s, %s)'
                        status = 'Pending'
                        insertVisitor = 'INSERT INTO beltline.visitor values (%s)'
                        insertEmail = 'INSERT INTO beltline.email values (%s, %s)'
                        cursor.execute(insertUser, (username, hashed_password, status, first_name, last_name))
                        conn.commit()
                        cursor.execute(insertVisitor, (username))
                        conn.commit()
                        for email in emails:
                            cursor.execute(insertEmail, (username, email))
                        conn.commit()
                except Exception as e:
                    print(e)
                    #return render_template('/error/500.html')
                    return redirect('/auth/login')


        return redirect('/auth/login')

@bp.route('/employee', methods=['GET', 'POST'])
def register_employee():
    if request.method == 'GET':
        return render_template('/register/register_employee.html')
    else:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password = request.form.get('password')
        emails = request.form.getlist('email[]')
        usertype = request.form.get('type')
        employeeID = random_with_N_digits(9)
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        hashed_password = generate_password_hash(password)

        conn = db.get_connection()
        with conn.cursor() as cursor:
            user = 'select username from user where username = %s'
            visitor = 'select username from visitor where username = %s'
            employee = 'select username from employee where username = %s'
            manager = 'select username from manager where username = %s'
            staff = 'select username from staff where username = %s'
            cursor.execute(user, (username))
            result1 = cursor.fetchone()
            cursor.execute(visitor, (username))
            result2 = cursor.fetchone()
            cursor.execute(employee, (username))
            result3 = cursor.fetchone()
            cursor.execute(manager, (username))
            result4 = cursor.fetchone()
            cursor.execute(staff, (username))
            result5 = cursor.fetchone()

            invalidEmail = False
            for eachEmail in emails:
                email = 'select email from email where email = %s'
                cursor.execute(email, (eachEmail))
                result = cursor.fetchone()
                if (result):
                    invalidEmail = True

            if (result1 or result2 or result3 or result4 or result5 or invalidEmail):
                print("you dumb")
                return redirect('/')
            else:
                try:
                    with conn.cursor() as cursor:
                        insertUser = 'INSERT INTO beltline.user values (%s, %s, %s, %s, %s)'
                        status = 'Pending'
                        insertEmail = 'INSERT INTO beltline.email values (%s, %s)'
                        insertEmployee = 'INSERT INTO beltline.employee values (%s, %s, %s, %s, %s, %s, %s)'
                        if usertype == 'manager':
                            insertManager = 'INSERT INTO beltline.manager values (%s)'
                        else:
                            insertStaff = 'INSERT INTO beltline.staff values (%s)'
                        cursor.execute(insertUser, (username, hashed_password, status, first_name, last_name))
                        conn.commit()
                        cursor.execute(insertEmployee, (username, employeeID, phone, address, city, state, zipcode))
                        conn.commit()
                        if usertype == 'manager':
                            cursor.execute(insertManager, (username))
                            conn.commit()
                        else:
                            cursor.execute(insertStaff, (username))
                            conn.commit()
                        for email in emails:
                            cursor.execute(insertEmail, (username, email))
                        conn.commit()
                except Exception as e:
                    print(e)
                    #return render_template('/error/500.html')
                    return redirect('/auth/login')

        return redirect('/auth/login')

@bp.route('/employee-visitor', methods=['GET', 'POST'])
def register_employee_visitor():
    if request.method == 'GET':
        return render_template('/register/register_employee-visitor.html')
    else:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password = request.form.get('password')
        emails = request.form.getlist('email[]')
        usertype = request.form.get('type')
        employeeID = random_with_N_digits(9)
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        conn = db.get_connection()
        with conn.cursor() as cursor:
            user = 'select username from user where username = %s'
            employee = 'select username from employee where username = %s'
            manager = 'select username from manager where username = %s'
            staff = 'select username from staff where username = %s'
            visitor = 'select username from visitor where username = %s'
            cursor.execute(user, (username))
            result1 = cursor.fetchone()
            cursor.execute(employee, (username))
            result2 = cursor.fetchone()
            cursor.execute(manager, (username))
            result3 = cursor.fetchone()
            cursor.execute(staff, (username))
            result4 = cursor.fetchone()
            cursor.execute(visitor, (username))
            result5 = cursor.fetchone()

            invalidEmail = False
            for eachEmail in emails:
                email = 'select email from email where email = %s'
                cursor.execute(email, (eachEmail))
                result = cursor.fetchone()
                if (result):
                    invalidEmail=True

            if (result1 or result2 or result3 or result4 or result5 or invalidEmail):
                print ("you dumb")
                return redirect('/')
            else:
                hashed_password = generate_password_hash(password)
                try:
                    with conn.cursor() as cursor:
                        insertUser = 'INSERT INTO beltline.user values (%s, %s, %s, %s, %s)'
                        status = 'Pending'
                        insertVisitor = 'INSERT Into beltline.visitor values (%s)'
                        insertEmail = 'INSERT INTO beltline.email values (%s, %s)'
                        insertEmployee = 'INSERT INTO beltline.employee values (%s, %s, %s, %s, %s, %s, %s)'
                        if usertype == 'manager':
                            insertManager = 'INSERT INTO beltline.manager values (%s)'
                        else:
                            insertStaff = 'INSERT INTO beltline.staff values (%s)'
                        cursor.execute(insertUser, (username, hashed_password, status, first_name, last_name))
                        conn.commit()
                        cursor.execute(insertEmployee, (username, employeeID, phone, address, city, state, zipcode))
                        conn.commit()
                        if usertype =='manager':
                            cursor.execute(insertManager, (username))
                            conn.commit()
                        else:
                            cursor.execute(insertStaff, (username))
                            conn.commit()
                        cursor.execute(insertVisitor, (username))
                        conn.commit()
                        for email in emails:
                            cursor.execute(insertEmail, (username, email))
                        conn.commit()
                except Exception as e:
                    print(e)
                    #return render_template('/error/500.html')
                    return redirect('/auth/login')

        return redirect('/auth/login')

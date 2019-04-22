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
        sql = 'select user.username, password, user_status as status from user join email on user.username = email.username where email = %s'
        with conn.cursor() as cursor:
            cursor.execute(sql, email)
            user = cursor.fetchone()
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        elif not user['status'] == 'Approved':
           error = 'Account not approved'

        if error is None:
            session.clear()
            session['username'] = user['username']
            session['role'] = getRole(user['username'])
            if session['role'] == 'manager' or session['role'] == 'manager-visitor':
                with conn.cursor() as cursor:
                    getSite = 'select name from site where manager = %s'
                    cursor.execute(getSite, session['username'])
                    result = cursor.fetchone()
                    if result:
                        session['site'] = result['name']
                        print(session['site'])
                    else:
                        session['site'] = ""
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

@bp.route('/manage/profile', methods=('GET', 'POST'))
def manage():
    conn = db.get_connection()
    if request.method == 'GET':
        username = session["username"]
        with conn.cursor() as cursor:
            getUser = 'SELECT FirstName as firstName, LastName as lastName, Username as username, EMPLOYEEID as employeeID, Phone as phone, Address as address, Zipcode as zip, State as state FROM ' \
            'beltline.employee JOIN beltline.user using(Username) WHERE username = %s'
            cursor.execute(getUser, session['username'])
            user = cursor.fetchone()
            getEmails = 'SELECT email from email where Username = %s'
            cursor.execute(getEmails, session['username'])
            emails = cursor.fetchall()
            email = emails[0]
            del emails[0]
            return render_template('/auth/manage_profile.html', data=user, em=email, emails=emails)
    else:
        username = session["username"]
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        phone = request.form.get('phone')
        emails = request.form.getlist('email')
        isVisitor = request.form.get('isVisitor')
        with conn.cursor() as cursor:
            #update first,last, - user table
            names = "UPDATE user SET FirstName = %s, LastName = %s WHERE Username = %s"
            cursor.execute(names, (first_name, last_name, username))
            conn.commit()
            #update phones - employee
            phones = "UPDATE employee SET Phone = %s WHERE Username = %s"
            cursor.execute(phones, (phone, username))
            conn.commit()
            #DELETE every row with username
            deleteemail = "DELETE from email where username = %s"
            cursor.execute(deleteemail, (username))
            conn.commit()
            for email in emails:
                #insert email, username into email (right order)
                insertemail = "INSERT into beltline.email values(%s, %s)"
                cursor.execute(insertemail, (username, email))
                conn.commit()
                if isVisitor == True:
                    #check if in visitor table (look take transit)
                    result = cursor.fetchone()
                    if not result:
                        #insert user into visitor table
                        something = "INSERT into visitor values(%s)"
                        cursor.execute(something, (username))
                else:
                #delete from visitor table
                    deleteuser = "DELETE from visitor where Username = %s"
                    cursor.execute(deleteuser, (username))
            return redirect('/auth/manage/profile')
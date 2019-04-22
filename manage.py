import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

def ifnull(var,value):
    if var == '' or var is None:
        return value
    else:
        return var.replace("'", "")


bp = Blueprint('manage', __name__, url_prefix='/manage')
@bp.route('/user', methods=['GET', 'POST'])
def user():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            manage = 'Select myview.username AS username, myview.EmailCount as emailcount, myview.Status as status, myview.UserType as usertype from myview'
            cursor.execute(manage)
            manage_user = cursor.fetchall()

            return render_template('manage_user.html', users=manage_user)
    else:
        print("post")
        user_type = request.form.get("usertype")
        username = request.form.get("username")
        status = request.form.get("status")
        print(type(user_type))
        print(type(username))
        print(type(status))
        with conn.cursor() as cursor:
            manage = 'Select myview.username AS username, myview.EmailCount as emailcount, myview.Status as status, myview.UserType as usertype ' \
            'from myview WHERE myview.username like %s AND myview.status like %s'
            cursor.execute(manage, (username, status))
            manage_user = cursor.fetchall()
            print(manage_user)

            return render_template('manage_user.html', users=manage_user)

@bp.route('/user/approved/<username>', methods=['GET'])
def approve(username):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            query = "UPDATE user SET User_Status = %s where username = %s"
            cursor.execute(query, ("Approved", username))
            return redirect('/manage/user')

@bp.route('/user/decline/<username>', methods=['GET'])
def decline(username):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            query = "UPDATE user SET User_Status = %s where username = %s"
            cursor.execute(query, ("Declined", username))
            return redirect('/manage/user')

@bp.route('/manage_staff', methods=['GET', 'POST'])
def manage_staff():
    conn = db.get_connection()
    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                containSite = request.form.get('site')
                firstName = request.form.get('firstName')
                lastName = request.form.get('lastName')
                startDate = request.form.get('startdate')
                endDate = request.form.get('enddate')

                getSites = 'select name from site'
                cursor.execute(getSites)
                sites = cursor.fetchall()

                getTableInfo = 'SELECT Concat(user.FirstName," ",user.LastName) AS "StaffName", '\
                                'staff_busy.Username, count(staff_busy.username) AS "EventShift", user.FirstName, user.LastName  '\
                                'FROM beltline.staff_busy NATURAL JOIN user  '\
                                'WHERE (StartDate between %s AND %s)   '\
                                'OR (EndDate between %s AND %s) AND  user.FirstName like %s AND user.LastName like %s '\
                                'GROUP BY Username;'


                cursor.execute(getTableInfo, (ifnull(startDate,"2001-01-01"), ifnull(endDate,"2040-01-01"), ifnull(startDate,"2001-01-01"), ifnull(endDate,"2040-01-01"), ifnull(firstName,"%"), ifnull(lastName,"%") ))
                info = cursor.fetchall()

                return render_template('manage_staff.html', sites=sites, names=info)
        except Exception as e:
            print(e)
    else:
        try:
            with conn.cursor() as cursor:
                getSites = 'select name from site'
                cursor.execute(getSites)
                sites = cursor.fetchall()
                getInfo = 'SELECT concat(user.FirstName," ",user.LastName) AS "StaffName", staff_busy.Username, count(staff_busy.username) AS "EventShift", user.FirstName, user.LastName FROM beltline.staff_busy NATURAL JOIN user GROUP BY Username'
                cursor.execute(getInfo)
                info = cursor.fetchall()

                return render_template('manage_staff.html', sites=sites, names=info)
        except Exception as e:
            print(e)

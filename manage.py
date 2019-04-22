import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('manage', __name__, url_prefix='/manage')
@bp.route('/user', methods=['GET', 'POST'])
def user():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            manage = "Select myview.username AS username, myview.EmailCount as emailcount, myview.Status as status, myview.UserType as usertype " \
            "from myview"
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
def approve():
    conn = db.get_connection()
    if request.method == 'GET':
        query = "UPDATE user SET User_Status = %s"
        cursor.execute(query, ("Approved"))
        return redirect('/manage/user')

@bp.route('/user/decline/<username>', methods=['GET'])
def decline():
    conn = db.get_connection()
    if request.method == 'GET':
        query = "UPDATE user SET User_Status = %s"
        cursor.execute(query, ("Declined"))
        return redirect('/manage/user')
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('event', __name__, url_prefix='/event')

#create() doesn't work
@bp.route('/create', methods=('GET', 'POST'))
def create():
    conn = db.get_connection()
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                name = request.form.get('name')
                price = request.form.get("price")
                capacity = request.form.get('capacity')
                minStaff = request.form.get('minstaff')
                startDate = request.form.get('startDate')
                endDate = request.form.get('endDate')

                assignStaff = 'for username in checked_staff:' \
                              'INSERT into assign_to(Username, %s, %s, siteName);'
                cursor.execute(assignStaff, (name, startDate))
                assignStaff = cursor.fetchall()
                print(assignStaff)

                return render_template('transit/create_event.html', staffData=assignStaff)
        except Exception as e:
            print(e)
    else:
        print("it was else block")
        try:
            with conn.cursor() as cursor:
                startDate = request.form.get('startDate')
                endDate = request.form.get('endDate')

                getAvailableStaff = 'SELECT staff.username, CONCAT(user.FirstName, ' ', user.LastName) FROM staff NATURAL JOIN ' \
                                     'user WHERE staff.username NOT IN (SELECT username FROM beltline.staff_busy' \
                                     'WHERE (StartDate between CAST(%s AS DATE) AND CAST(%s AS DATE)) ' \
                                     'OR (EndDate between CAST(%s AS DATE) AND CAST(%s AS DATE)))'
                cursor.execute(getAvailableStaff, (startDate, endDate, startDate, endDate))
                availableStaff = cursor.fetchall()

                return render_template('transit/create_event.html', staffData=availableStaff)
        except Exception as e:
            print(e)

# @bp.route('/create', methods=('GET', 'POST'))
# def edit():
#     conn = db.get_connection()

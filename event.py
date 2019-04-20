import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('event', __name__, url_prefix='/event')


#fix me
@bp.route('/create', methods=('GET', 'POST'))
def create():
    conn = db.get_connection()
    if request.method == 'POST':
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

                return render_template('/event/create_event.html', staffData=assignStaff)
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
                cursor.execute(getAvailableStaff, ('01-01-1999', '01-01-2018', '01-01-1999', '01-01-2018'))
                availableStaff = cursor.fetchall()

                return render_template('/event/create_event.html', staffData=availableStaff)
        except Exception as e:
            print(e)

#fix me
@bp.route('/explore', methods=('GET', 'POST'))
def explore():
    conn = db.get_connection()
    if request.method == "GET":
        try:
            with conn.cursor() as cursor:
                # name = request.form.get('name')
                # desc = request.form.get('desc')
                siteName = request.form.get('site')
                # startDate = request.form.get('startDate')
                # endDate = request.form.get('endDate')
                # minVisit = request.form.get('minVisit')
                # maxVisit = request.form.get('maxVisit')
                # minPrice = request.form.get('minPrice')
                # maxVisit = request.form.get('maxVisit')

                getSites = 'select Name as siteName from site'
                cursor.execute(getSites)
                sites = cursor.fetchall()
                print(sites)

                return render_template('/event/explore_event.html', sites=sites)
        except Exception as e:
            print(e)
    else:
        # with conn.cursor() as cursor:
            # name = request.form.get('name')
            # desc = request.form.get('desc')
            # siteName = request.form.get('siteName')
            # startDate = request.form.get('startDate')
            # endDate = request.form.get('endDate')
            # minVisit = request.form.get('minVisit')
            # maxVisit = request.form.get('maxVisit')
            # minPrice = request.form.get('minPrice')
            # maxVisit = request.form.get('maxVisit')

            # getSites = 'select name from site'
            # cursor.execute(getSites)
            # sites = cursor.fetchall()

            return render_template('/')



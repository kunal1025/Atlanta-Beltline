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

@bp.route('/visitor/detail/<name>/<start_date>/<site_name>', methods=('GET', 'POST'))
def getDetail(name, start_date, site_name):
    conn = db.get_connection()
    username = session['username']
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getEvent = 'select test2.username, test1.Name as eventName, test1.SiteName as siteName, test1.Price as price, '\
            '(test2.capacity - test1.TotalVisits) AS ticketRemaining , test1.StartDate as startDate, '\
            'test1.EndDate as endDate, test1.description from test1 natural join test2 '\
            'Where username = %s AND test1.Name = %s AND '\
            'test1.SiteName = %s and test1.StartDate = %s '\
            'group by Name, SiteName, Startdate;'
            cursor.execute(getEvent, (username, name, site_name, start_date))
            event = cursor.fetchone()
            return render_template('/details/visitor_event_detail.html', event=event)
    else:
        visit_date = request.form.get('visitDate')

#@bp.route('/staff/detail/<name>/<start_date>/<site_name>', methods=('GET',))

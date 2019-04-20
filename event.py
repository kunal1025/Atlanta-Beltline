import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('event', __name__, url_prefix='/event')

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

                # if (startDate < endDate):
                #     print("Start Date should come before End Date")

                # getSites = 'select name as siteName from site'
                # cursor.execute(getSites)
                # sites = cursor.fetchall()

                getAssignStaffList = 'SELECT staff.username as name, CONCAT(user.FirstName, ' ', user.LastName) FROM staff NATURAL JOIN ' \
                                     'user WHERE staff.username NOT IN (SELECT username FROM beltline.staff_busy' \
                                     'WHERE (StartDate between CAST(%s AS DATE) AND CAST(%s AS DATE)) ' \
                                     'OR (EndDate between CAST(%s AS DATE) AND CAST(%s AS DATE)))'
                cursor.execute(getAssignStaffList, (startDate, endDate, startDate, endDate))
                assignStaffList = cursor.fetchall()

                return render_template('transit/manage_transit.html', data=assignStaffList)
        except Exception as e:
            print(e)
    else:
        try:
            with conn.cursor() as cursor:
                getSites = 'select name as siteName from site'
                cursor.execute(getSites)
                sites = cursor.fetchall()

                # getTableInfo = 'SELECT TransitType as transportType, TransitRoute as route, Count(Distinct(SiteName)) as numConnectedSites, ' \
                #                'count(Distinct(username)) as numTransitLogged, Price as price from connect join transit using(TransitType, TransitRoute)' \
                #                'join take using(TransitType, TransitRoute) group by concat(TransitType, TransitRoute)'
                # cursor.execute(getTableInfo)
                # info = cursor.fetchall()

                return render_template('transit/manage_transit.html', sites=sites, routes={})
        except Exception as e:
            print(e)
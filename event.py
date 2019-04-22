import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('event', __name__, url_prefix='/event')

def ifnull(var,value):
    if var == '' or var is None:
        return value
    else:
        return var.replace("'", "")

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

                getAvailableStaff = 'SELECT staff.username, CONCAT(user.FirstName, user.LastName) as name FROM staff NATURAL JOIN user '
                                     #'WHERE staff.username NOT IN (SELECT username FROM beltline.staff_busy'
                                     #'WHERE (StartDate between CAST(%s AS DATE) AND CAST(%s AS DATE)) ' \
                                     #'OR (EndDate between CAST(%s AS DATE) AND CAST(%s AS DATE)))'
                cursor.execute(getAvailableStaff)
                availableStaff = cursor.fetchall()
                print(availableStaff)
                return render_template('/event/create_event.html', staffData=availableStaff)
        except Exception as e:
            print(e)



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

@bp.route('/explore_event', methods=('GET', 'POST'))
def explore_event():
    conn = db.get_connection()
    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                getAllSites = 'SELECT name from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()

                name = request.form.get("name")
                desc = request.form.get("desc")
                desc1 = "%" + desc + "%"
                startDate = request.form.get('startdate')
                endDate = request.form.get('enddate')
                priceMin = request.form.get('priceMin')
                priceMax = request.form.get('priceMax')
                visitMin = request.form.get('visitMin')
                visitMax = request.form.get('visitMax')
                visited = request.form.get('site')
                sold_out = request.form.get('site1')
                containSite = request.form.get('siteName')



                getData = 'select A.Name, A.SiteName, A.TicketPrice, A.TicketRemaining, A.TotalVisits, B.MyVisits, A.StartDate, A.EndDate, A.description from  '\
                            '(select test1.description, test1.EndDate, test1.StartDate, test1.Name, test1.SiteName, test1.Price as `TicketPrice`, (test2.capacity - test1.TotalVisits) AS `TicketRemaining` , test1.TotalVisits, count(username) AS `MyVisits` from test1 natural join test2  '\
                            'group by Name, SiteName, Startdate)  '\
                            'AS A  '\
                            'Join  '\
                            '(  '\
                            'select test1.Name, test1.SiteName, count(username) AS `MyVisits` from test1 natural join test2  '\
                            'Where username = "visitor1"  '\
                            'group by Name, SiteName, Startdate  '\
                            'UNION  '\
                            'select Distinct VisitEventName as Name, SiteName, "0" as MyVisits from visit_event  '\
                            'Where NOT concat(SiteName,StartDate,VisitEventName) in (Select concat(SiteName,StartDate,VisitEventName)e from visit_event Where username = "visitor1"))  '\
                            'AS B  '\
                            'on B.Name = A.Name AND A.SiteName = B.SiteName '\
                            'WHERE A.Name like %s AND A.description like %s AND A.SiteName like %s AND A.StartDate like %s AND A.EndDate like %s AND '\
                            '(A.TotalVisits BETWEEN %s AND %s) AND (A.TicketPrice BETWEEN %s AND %s) AND (B.MyVisits <= %s) AND A.TicketRemaining >= %s'

                cursor.execute(getData, (ifnull(name, "%"), ifnull(desc1,"%"), ifnull(containSite, "%"), ifnull(startDate, "%"), ifnull(endDate, "%"), ifnull(visitMin, "0"), ifnull(visitMax,"10000000"), ifnull(priceMin,"0"), ifnull(priceMax, "1000000"),visited, sold_out))
                info = cursor.fetchall()

                print(info)
                return render_template('event/explore_event.html', sites = sites, EventDB = info)
        except Exception as e:
            print(e)
            return 'bad1'
    else:
        try:
            with conn.cursor() as cursor:
                getAllSites = 'SELECT name from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()



                getData = 'select A.Name, A.SiteName, A.TicketPrice, A.TicketRemaining, A.TotalVisits, B.MyVisits from  '\
                            '(select test1.Name, test1.SiteName, test1.Price as `TicketPrice`, (test2.capacity - test1.TotalVisits) AS `TicketRemaining` , test1.TotalVisits, count(username) AS `MyVisits` from test1 natural join test2  '\
                            'group by Name, SiteName, Startdate)  '\
                            'AS A  '\
                            'Join  '\
                            '(  '\
                            'select test1.Name, test1.SiteName, count(username) AS `MyVisits` from test1 natural join test2  '\
                            'Where username = "visitor1"  '\
                            'group by Name, SiteName, Startdate  '\
                            'UNION  '\
                            'select Distinct VisitEventName as Name, SiteName, "0" as MyVisits from visit_event  '\
                            'Where NOT concat(SiteName,StartDate,VisitEventName) in (Select concat(SiteName,StartDate,VisitEventName)e from visit_event Where username = "visitor1"))  '\
                            'AS B  '\
                            'on B.Name = A.Name AND A.SiteName = B.SiteName'

                cursor.execute(getData)
                info = cursor.fetchall()
                print(info)
                print('GET')
                return render_template('event/explore_event.html', sites = sites, EventDB = info)
        except Exception as e:
            print(e)
            return 'bad2'
@bp.route('/manage', methods=('GET', 'POST'))
def manage():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getEvents = 'Select B.Name as name, A.StaffCount, A.Duration, B.TotalVisits, B.Revenue, A.StartDate FROM '\
                '( '\
                'SELECT Name, count(Username) AS StaffCount, datediff(event.EndDate, event.StartDate) '\
                'AS Duration, event.SiteName, event.StartDate FROM assign_to join event using(Name, SiteName, StartDate) group by Name, SiteName, StartDate '\
                ') '\
                'AS A '\
                'JOIN '\
                '( '\
                'SELECT event.Name, event.StartDate, event.SiteName ,count(Username) AS "TotalVisits", count(Username)*Price AS '\
                '"Revenue" from beltline.event JOIN visit_event on event.Name = visit_event.VisitEventName AND '\
                'event.StartDate = visit_event.StartDate GROUP BY visit_event.VisitEventName, visit_event.StartDate, event.siteName '\
                ') '\
                'AS B '\
                'ON A.Name = B.Name AND A.StartDate = B.StartDate AND A.SiteName = B.SiteName'
            cursor.execute(getEvents)
            events = cursor.fetchall()
            return render_template('/event/manage_event.html', events=events)
    else:
        name = request.form.get('name')
        description = request.form.get('description')
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        minDuration = request.form.get('minDuration')
        maxDuration = request.form.get('maxDuration')
        minVisit = request.form.get('minVisit')
        maxVisit = request.form.get('maxVisit')
        minRevenue = request.form.get('minRevenue')
        maxRevenue = request.form.get('maxRevenue')

        siteName = session['site']
        with conn.cursor() as cursor:
            getEvents = 'Select B.Name as name, A.StaffCount as staffCount, A.Duration, B.TotalVisits, B.Revenue, A.StartDate FROM '\
                '( '\
                'SELECT Name, count(Username) AS StaffCount, datediff(event.EndDate, event.StartDate) '\
                'AS Duration, event.SiteName, event.StartDate FROM assign_to join event using(Name, SiteName, StartDate) group by Name, SiteName, StartDate '\
                ') '\
                'AS A '\
                'JOIN '\
                '( '\
                'SELECT event.Name, event.StartDate, event.EndDate, event.SiteName ,count(Username) AS "TotalVisits", count(Username)*Price AS '\
                '"Revenue" from beltline.event JOIN visit_event on event.Name = visit_event.VisitEventName AND '\
                'event.StartDate = visit_event.StartDate GROUP BY visit_event.VisitEventName, visit_event.StartDate, event.siteName '\
                ') '\
                'AS B '\
                'ON A.Name = B.Name AND A.StartDate = B.StartDate AND A.SiteName = B.SiteName WHERE A.SiteName = %s AND A.StartDate between %s AND "2100-02-09" AND B.EndDate '\
                'between "2001-02-09" AND %s AND Duration between %s AND %s '\
                'AND TotalVisits Between %s AND %s AND Revenue between %s AND %s'
            cursor.execute(getEvents, (siteName, startDate, endDate, minDuration, maxDuration, minVisit, maxVisit, minRevenue, maxRevenue))
            events = cursor.fetchall()
            return render_template('/event/manage_event.html', events=events)

@bp.route('/edit/<name>/<startDate>', methods=('GET', 'POST'))
def edit(name, startDate):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getEvent = 'select sitename, name, startDate, endDate, price, minstaffreq, capacity, description from event where name = %s AND startdate = %s'
            cursor.execute(getEvent, (name, startDate))
            event = cursor.fetchone()
            getStaff = 'SELECT FirstName, LastName, concat(FirstName, " ", LastName) AS name '\
            'FROM assign_to JOIN event USING '\
            '(Name, SiteName, StartDate) JOIN user Using(Username) '\
            'WHERE event.StartDate = %s AND event.EndDate = %s AND SiteName = %s'
            cursor.execute(getStaff, (startDate, event['endDate'], event['sitename']))
            staff = cursor.fetchall()
            for s in staff:
                s['checked'] = 1
            getAvailableStaff = 'SELECT staff.username, CONCAT(user.FirstName, " ", user.LastName) as name FROM staff NATURAL JOIN '\
            'user WHERE staff.username NOT IN (SELECT username FROM beltline.staff_busy '\
            'WHERE (StartDate between %s AND %s) OR (EndDate between %s AND %s))'
            startDate = event['startDate']
            endDate = event['endDate']
            cursor.execute(getAvailableStaff, (startDate, endDate, startDate, endDate))
            availableStaff = cursor.fetchall()
            print(staff)
            staff.append(availableStaff)
            getResults = ''
            return render_template('/event/view_edit_event.html', data=event, staff=staff)

@bp.route('/delete/<name>/<startDate>', methods=('GET',))
def delete(name, startDate):
    conn = db.get_connection()
    with conn.cursor() as cursor:
        deleteEvent = 'delete from event where name = %s AND startdate = %s'
        cursor.execute(deleteEvent, (name, startDate))
        conn.commit()
        redirect('/edit/' + name + '/' + startDate)

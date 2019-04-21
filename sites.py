import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
import db

def ifnull(var,value):
    if var == '' or var is None:
        return value
    else:
        return var.replace("'", "")

bp = Blueprint('sites', __name__, url_prefix='/site')
@bp.route('/edit/<SiteName>', methods=['GET', 'POST'])
# THE HTML IS INCORRECT
def edit(SiteName):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            siteinfo = "select FirstName, LastName, Address, Zipcode, Manager, OpenEveryDay from site JOIN user on site.Manager = user.Username where Name = %s"
            cursor.execute(siteinfo, (SiteName,))

            manager_drop_down = "SELECT concat(FirstName,' ',LastName) from manager join user using(Username) "\
            "where username not in (Select username from beltline.site join manager on manager.Username = site.Manager)"
            current_manager = "SELECT concat(FirstName,' ',LastName) from manager join user using(Username) join site on manager.Username = site.Manager WHERE name = %s"
            
            cursor.execute(manager_drop_down)
            info = cursor.fetchall()
            
            cursor.execute(current_manager, (SiteName,))
            drop_down = cursor.fetchone()
            drop_down["is_selected"] = 1
            
            info.append(drop_down)
            return render_template('site/edit_site.html', data=siteinfo, manager=info)
    else:
        name = request.form.get('name')
        zip_code = request.form.get("zipcode")
        address = request.form.get('address')
        manager = request.form.get('manager')
        openEveryday = request.form.get('openeveryday')
        with conn.cursor as cursor:
            edit_site = "UPDATE beltline.site SET Name = %s , Address = %s,"\
            "manager = %s, Zipcode = %s, OpenEveryDay = %s WHERE site.Name = %s"
            cursor.execute(edit_site, (name, zip_code, address, manager, openEveryday))
            conn.commit()

    return redirect('/edit/' + SiteName)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:

            manager = "SELECT concat(FirstName,' ',LastName) from manager join user using(Username)"\
            "where username not in (Select username from beltline.site join manager on manager.Username = site.Manager)"
            cursor.execute(manager)

            return render_template('site/create_site.html', manager=manager)
    else:
        newname = request.form.get('name')
        newzip = request.form.get("zipcode")
        newaddress = request.form.get('address')
        newmanager = request.form.get('manager')
        newopen = request.form.get('openeveryday')
        with conn.cursor as cursor:
            edit_site = "INSERT into beltline.site values(%s, %s, %s, %s, %s)"
            cursor.execute(edit_site, (newname, newaddress, newzip, newopen, newmanager))
            conn.commit()

    return redirect('/')
    
@bp.route('/detail/<Name>', methods=['GET'])
def detail(Name):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getALLSITES = "SELECT Name as site, OpenEveryDay as openEveryday, concat(Address, ', Zipcode) as address FROM beltline.site"
            cursor.execute(getALLSITES)
            sites = cursor.fetchone()
        return redirect('sites/site_detail.html', data=sites)
    else:
        with conn.cursor() as cursor:
            sitedate = "INSERT into visit_site (%s, %s, %s)"
            cursor.execute(sitedate, (Username, SiteName, Date))
            conn.commit()
            sitedate = cursor.fetchone()

    





#38
@bp.route('/history', methods=('GET','POST'))
def history():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            username = session["username"]
            startdate = request.form.get("startdate")
            enddate = request.form.get("enddate")
            eventname = request.form.get("event")

            visit_history = "(SELECT VisitEventDate AS date, VisitEventName AS event, Event.SiteName AS site, Price from visit_event join event ON event.Name = visit_event.VisitEventName AND event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate WHERE username = %s AND event.StartDate >= %s AND event.EndDate <= %s AND event.Name = %s) UNION (SELECT Date, '' AS VisitEventName, Name AS SiteName, '0' AS Price from site join visit_site on visit_site.SiteName = site.Name WHERE username = %s)"

            cursor.execute(visit_history, (username, ifnull(startdate, "%"), ifnull(enddate, "%"), ifnull(eventname, "%"), username))
            visit_history = cursor.fetchall()

            sites_query = "SELECT site.Name AS site from beltline.site"
            cursor.execute(sites_query)
            sites = cursor.fetchall()

        return render_template('visit_history.html', data=visit_history, sites=sites)

# 32
@bp.route('/staffeventdetail', methods=['GET'])
def event_detail():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            query = "Select FirstName, LastName, concat(FirstName, LastName) AS staffName,Name AS eventName, SiteName AS siteName, StartDate as startDate, EndDate AS endDate, capacity, datediff(EndDate, StartDate) as durationDays, price, description as 'desc' FROM assign_to JOIN user using (Username) JOIN event using (SiteName, Name, StartDate)"
            cursor.execute(query)
            data = cursor.fetchall()

            return render_template('details/staff_event_detail.html',event=data)
 
#30
@bp.route('/dailydetail', methods=['GET'])
def daily_detail():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:

            startdate = "2019-02-04"
            enddate = "2019-02-11"

            query = "SELECT VisitEventName, count(Username) AS Visit, price, price*count(Username) AS "\
            "Revenue FROM event JOIN visit_event ON event.Name = visit_event.VisitEventName AND "\
            "event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate WHERE "\
            "event.StartDate >= %s AND event.EndDate <= %s "\
            "GROUP BY Event.SiteName, VisitEventDate, event.StartDate"
 

            cursor.execute(query, (startdate, enddate))
            data = cursor.fetchall()

            return render_template('details/daily_detail.html',data=data)

#36
@bp.route('/transitdetail', methods=['GET'])
def transit_detail():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:

            #sitename = 
            #transporttype =

            query = "SELECT TransitType, TransitRoute, Price, count(*) FROM beltline.transit JOIN "\
            "beltline.connect using(TransitType, TransitRoute) "\
            "WHERE SiteName = %s AND TransitType = %s "\
            "GROUP BY concat(transitType, TransitRoute);

            cursor.execute(query (sitename, transporttype))
            data = cursor.fetchall()

            return render_template('transit/transit_detail.html',data=data)
 
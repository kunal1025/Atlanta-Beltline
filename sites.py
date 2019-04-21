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
            siteinfo = "select Address, Zipcode, Manager, OpenEveryDay from site JOIN user on site.Manager = user.Username where Name = %s"
            cursor.execute(siteinfo, (SiteName,))

            manager_drop_down = "SELECT FirstName, LastName, concat(FirstName,' ',LastName) as Name from manager join user using(Username) "\
            "where username not in (Select username from beltline.site join manager on manager.Username = site.Manager)"
            current_manager = "SELECT concat(FirstName,' ',LastName) from manager join user using(Username) join site on manager.Username = site.Manager WHERE name = %s"
            
            cursor.execute(manager_drop_down)
            manager_info = cursor.fetchall()
            
            cursor.execute(current_manager, (SiteName,))
            drop_down = cursor.fetchone()
            drop_down["is_selected"] = 1
            
            manager_info.append(drop_down)
            return render_template('site/edit_site.html', data=siteinfo, managers=manager_info)
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
            manager_query = "SELECT FirstName, LastName, concat(FirstName,' ',LastName) as Name, username from manager join user using(Username)"\
            "where username not in (Select username from beltline.site join manager on manager.Username = site.Manager)"
            cursor.execute(manager_query)
            managers = cursor.fetchall() 

            return render_template('site/create_site.html', managers=managers)
    else:
        newname = request.form.get('name')
        newzip = request.form.get("zipcode")
        newaddress = request.form.get('address')
        newmanager = request.form.get('manager')
        newopen = request.form.get('openeveryday')
        with conn.cursor as cursor:
            manager_username = "SELECT username from Manager join user using(Username) where SELECT username from Manager join user using(Username) where(concat(FirstName, ' ', LastName) = %s"
            cursor.execute(manager_username, (newmanager,))

            edit_site = "INSERT into beltline.site values(%s, %s, %s, %s, %s)"
            cursor.execute(edit_site, (newname, newaddress, newzip, newopen, newmanager))
            conn.commit()

        return redirect('/create')
    
@bp.route('/detail/<Name>', methods=['GET'])
def detail(Name):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getALLSITES = "SELECT Name as site, OpenEveryDay as openEveryday, concat(Address,' ', Zipcode) as address FROM beltline.site"
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
            getSites = siteSQL = 'SELECT name FROM site'
            cursor.execute(getSites)
            sites = cursor.fetchall()
            print(sites)
            return render_template('/transit/transit_history.html', sites=sites)

    else:
        with conn.cursor() as cursor:
            username = session["username"]
            startdate = request.form.get("startdate")
            enddate = request.form.get("enddate")
            eventname = request.form.get("event")

            getSites = siteSQL = 'SELECT name FROM site'
            cursor.execute(getSites)
            sites = cursor.fetchall()

            visit_history = "(SELECT VisitEventDate AS date, VisitEventName AS event, Event.SiteName AS siteName, " \
            "Price AS price from visit_event join event ON event.Name = visit_event.VisitEventName AND event.SiteName = visit_event.SiteName " \
            "AND event.StartDate = visit_event.StartDate WHERE username = %s AND event.StartDate between %s AND '2100-02-09' AND " \
            "event.EndDate between '2001-02-09' AND %s AND event.Name like %s) UNION (SELECT Date, '' AS VisitEventName, Name AS " \
            "SiteName, '0' AS Price from site join visit_site on visit_site.SiteName = site.Name WHERE username = %s)"

            cursor.execute(visit_history, (username, ifnull(startdate, "2000-02-01"), ifnull(enddate, "2200-01-01"), ifnull(eventname, ""), username))
            visit_history = cursor.fetchall()
            print(visit_history)
            return render_template('visit_history.html', history=visit_history, sites=sites)

# 32
@bp.route('/staffeventdetail/<SiteName>/<Name>/<StartDate>', methods=('GET',))
def event_detail(SiteName, Name, StartDate):
    conn = db.get_connection()
    with conn.cursor() as cursor:
        query = "Select FirstName, LastName, concat(FirstName, LastName) AS staffName,Name AS eventName, " \
        "SiteName AS siteName, StartDate as startDate, EndDate AS endDate, capacity, datediff(EndDate, StartDate) " \
        "as durationDays, price, description as 'desc' FROM assign_to JOIN user using (Username) JOIN event using" \
        "(SiteName, Name, StartDate) WHERE assign_to.SiteName = %s AND assign_to.StartDate = %s AND assign_to.Name = %s"
        
        cursor.execute(query, (SiteName, StartDate, Name))
        data = cursor.fetchall()
        return render_template('details/staff_event_detail.html',event=data)
 
#30
@bp.route('/dailydetail', methods=['GET'])
def daily_detail():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:

            visitdate = "2019-02-04"
            sitename = session
            

            query = "SELECT VisitEventName AS eventName, group_concat(Distinct concat(User.FirstName, ' ', User.LastName)) as staffNames, " \ 
            "count(visit_event.Username) AS visits, price, price*count(visit_event.Username) as " \
            "revenue from event join visit_event on event.Name = visit_event.VisitEventName AND " \
            "event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate JOIN " \
            "assign_to ON assign_to.Name = event.Name AND assign_to.SiteName = event.SiteName AND " \
            "assign_to.StartDate = event.StartDate JOIN user on user.Username = assign_to.Username " \
            "WHERE visit_event.StartDate = %s AND site_name = %s " \
            "group by concat Event.SiteName, VisitEventDate, event.StartDate"


            cursor.execute(query, (visitdate, sitename))
            data = cursor.fetchall()

            return render_template('details/daily_detail.html',dataDB=data)

#36
@bp.route('/transitdetail/<SiteName>/<TransitType>', methods=['GET'])
def transit_detail(SiteName, TransitType):
    conn = db.get_connection()
    if request.method == 'GET':
        return render_template('transit/transit_detail.html')

    else:

            sitename = "Inman Park"
            transittype = "Bus"

            query = "SELECT TransitType, TransitRoute, Price, count(*) FROM beltline.transit JOIN "\
            "beltline.connect using(TransitType, TransitRoute) "\
            "WHERE SiteName = %s AND TransitType = %s "\
            "GROUP BY TransitType, TransitRoute"

            cursor.execute(query (sitename, transittype))
            data = cursor.fetchall()

            return render_template('transit/transit_detail.html', transit=data)
 
 #35

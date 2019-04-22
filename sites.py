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
            sites = "select Name AS name, Address AS address, Zipcode as zipcode, Manager as manager, OpenEveryDay from site JOIN user on site.Manager = user.Username where Name = %s"
            cursor.execute(sites, (SiteName,))
            siteinfo = cursor.fetchone()

            manager_drop_down = "SELECT FirstName, LastName, concat(FirstName,' ',LastName) as Name from manager join user using(Username) " \
            "where username not in (Select username from beltline.site join manager on manager.Username = site.Manager) "

            current_manager = "SELECT concat(FirstName,' ',LastName) from manager join user using(Username) join site on manager.Username = site.Manager WHERE name = %s"
            
            cursor.execute(manager_drop_down)
            manager_info = cursor.fetchall()
            
            cursor.execute(current_manager, (SiteName,))
            drop_down = cursor.fetchone()

            print(drop_down)
            drop_down["is_selected"] = 1
            manager_info.append(drop_down)

            print(siteinfo)
            return render_template('site/edit_site.html', data=siteinfo, managers=manager_info)
    else:
        name = request.form.get('name')
        zip_code = request.form.get('zipcode')
        address = request.form.get('address')
        manager = request.form.get('manager')
        openEveryday = request.form.get('openEveryday')
        with conn.cursor() as cursor:
            manager_username = "SELECT username from Manager join user using(Username) where(concat(FirstName, ' ', LastName)) = %s"
            cursor.execute(manager_username, (manager,))
            print(zip_code)
            edit_site = "UPDATE beltline.site `Address` = %s," \
            "Manager = %s, Zipcode = %s, OpenEveryDay = %s WHERE site.Name = %s"
            cursor.execute(edit_site, (address, manager, zip_code, openEveryday, name))
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
        newopen = request.form.get('type')
        with conn.cursor() as cursor:
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

    return redirect('sites/site_detail.html', data=sites)
    
@bp.route('/manage_site', methods=('GET', 'POST'))
def manage_site():
    conn = db.get_connection()
    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                getAllSites = 'SELECT name from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()

                getAllManagers = '(SELECT username as name from manager join user using(Username) '\
                                    'where username in '\
                                    '(Select username from beltline.site join manager on manager.Username = site.Manager))'
                cursor.execute(getAllManagers)
                managers = cursor.fetchall()

                containSite = request.form.get('site')
                selectedManager = request.form.get('manager')
                print(selectedManager)
                openeveryDay = request.form.get('type')
                print(openeveryDay)

                getData = 'SELECT name, manager, OpenEveryDay from beltline.site ' \
                            'WHERE name like %s AND manager like %s AND OpenEveryDay like %s'

                cursor.execute(getData,(ifnull(containSite,"%"), ifnull(selectedManager, "%"), ifnull(openeveryDay, "%")))
                info = cursor.fetchall()

                print(info)
                return render_template('site/manage_site.html', sites = sites, managers = managers, names = info)
        except Exception as e:
            print(e)
            return 'bad1'
    else:
        try:
            with conn.cursor() as cursor:
                getAllSites = 'SELECT name from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()
                print(sites)

                getAllManagers = '(SELECT username as name from manager join user using(Username) '\
                                    'where username in '\
                                    '(Select username from beltline.site join manager on manager.Username = site.Manager))'
                cursor.execute(getAllManagers)
                managers = cursor.fetchall()
                print(managers)

                getData = 'SELECT name, manager, OpenEveryDay from beltline.site '

                cursor.execute(getData)
                info = cursor.fetchall()

                print('GET')
                return render_template('site/manage_site.html', sites = sites, managers = managers, names = info)
        except Exception as e:
            print(e)
            return 'bad2'

@bp.route('/site_report', methods=('GET', 'POST'))
def site_report():
    conn = db.get_connection()
    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                startDate = request.form.get('startdate')
                endDate = request.form.get('enddate')
                eventMin = request.form.get('eventMin')
                eventMax = request.form.get('eventMax')
                staffMin = request.form.get('staffMin')
                staffMax = request.form.get('staffMax')
                revMin = request.form.get('revMin')
                revMax = request.form.get('revMax')
                visitMin = request.form.get('visitMin')
                visitMax = request.form.get('visitMax')

                getData = 'SELECT A.VisitEventDate as "date", A.EventCount, A.StaffCount, (A.EventVisits + B.SiteVisits) AS "TotalVisits", '\
                            'A.EventCount*Price AS "TotalRevenue" FROM (select visit_event.VisitEventDate, count(event.Name) as '\
                            '"EventCount", count(assign_to.Username) AS "StaffCount", count(visit_event.Username) AS "EventVisits", '\
                            'Price from assign_to JOIN event using (Name, SiteName, StartDate) JOIN visit_event ON '\
                            'event.Name = visit_event.VisitEventName AND event.SiteName = visit_event.SiteName '\
                            'AND event.StartDate = visit_event.StartDate GROUP BY (visit_event.VisitEventDate)) as A JOIN '\
                            '(select visit_site.Date, count(visit_site.Username) AS "SiteVisits" FROM site JOIN visit_site on site.Name = '\
                            'visit_site.SiteName GROUP BY (visit_site.date)) AS B ON A.VisitEventDate = B.Date '\
                            'WHERE (EventCount BETWEEN %s AND %s) AND (StaffCount BETWEEN %s AND %s) AND ((EventVisits + SiteVisits) BETWEEN %s AND %s) '\
                            'AND ((A.EventCount*Price) BETWEEN %s AND %s) AND (VisitEventDate BETWEEN %s AND %s)'
                cursor.execute(getData, (ifnull(eventMin,"0"), ifnull(eventMax,"10000"), ifnull(staffMin,"0"), ifnull(staffMax,"10000"), ifnull(visitMin,"0"), ifnull(visitMax,"10000"), ifnull(revMin,"0"), ifnull(revMax,"10000"), ifnull(startDate,"0"), ifnull(endDate,"10000")))
                info = cursor.fetchall()

                print(info)
                return render_template('site/site_report.html', dataDB = info)
        except Exception as e:
            print(e)
            return 'bad1'
    else:
        try:
            with conn.cursor() as cursor:
                getData = 'SELECT A.VisitEventDate as "date", A.EventCount, A.StaffCount, (A.EventVisits + B.SiteVisits) AS "TotalVisits", '\
                            'A.EventCount*Price AS "TotalRevenue" FROM (select visit_event.VisitEventDate, count(event.Name) as '\
                            '"EventCount", count(assign_to.Username) AS "StaffCount", count(visit_event.Username) AS "EventVisits", '\
                            'Price from assign_to JOIN event using (Name, SiteName, StartDate) JOIN visit_event ON '\
                            'event.Name = visit_event.VisitEventName AND event.SiteName = visit_event.SiteName '\
                            'AND event.StartDate = visit_event.StartDate GROUP BY (visit_event.VisitEventDate)) as A JOIN '\
                            '(select visit_site.Date, count(visit_site.Username) AS "SiteVisits" FROM site JOIN visit_site on site.Name = '\
                            'visit_site.SiteName GROUP BY (visit_site.date)) AS B ON A.VisitEventDate = B.Date '

                cursor.execute(getData)
                info = cursor.fetchall()
                print('GET')
                return render_template('site/site_report.html', dataDB = info)
        except Exception as e:
            print(e)
            return 'bad2'
    
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
@bp.route('/dailydetail/<VisitEventDate>', methods=['GET'])
def daily_detail():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:

            sitename = session["site"]
            
            query = "SELECT VisitEventName AS eventName, group_concat(Distinct concat(User.FirstName, ' ', User.LastName)) as staffNames, " \
            "count(visit_event.Username) AS visits, Price, Price*count(visit_event.Username) as " \
            "revenue from event join visit_event on event.Name = visit_event.VisitEventName AND " \
            "event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate JOIN " \
            "assign_to ON assign_to.Name = event.Name AND assign_to.SiteName = event.SiteName AND " \
            "assign_to.StartDate = event.StartDate JOIN user on user.Username = assign_to.Username " \
            "WHERE visit_event.VisitEventDate = %s AND visit_event.SiteName = %s " \
            "group by event.SiteName, visit_event.VisitEventDate, event.StartDate"

            cursor.execute(query, (VisitEventDate, sitename))
            data = cursor.fetchall()
            print(data)
            return render_template('details/daily_detail.html',dataDB=data)

#36
@bp.route('/transitdetail/<SiteName>/<TransitType>', methods=['GET'])
def transit_detail(SiteName, TransitType):
    conn = db.get_connection()
    if request.method == 'GET':
        return render_template('transit/transit_detail.html', SiteName=SiteName)

    else:
            query = "SELECT SiteName as site, TransitType, TransitRoute, Price, count(*) FROM beltline.transit AS cs JOIN "\
            "beltline.connect using(TransitType, TransitRoute) "\
            "WHERE SiteName = %s AND TransitType = %s "\
            "GROUP BY TransitType, TransitRoute"

            cursor.execute(query (SiteName, TransitType))
            transits = cursor.fetchall()

            return render_template('transit/transit_detail.html', transits=data)
 


@bp.route('/explore_site', methods=('GET', 'POST'))
def explore_site():
    conn = db.get_connection()
    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                getAllSites = 'SELECT name from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()

                startDate = request.form.get('startdate')
                endDate = request.form.get('enddate')
                eventMin = request.form.get('eventMin')
                eventMax = request.form.get('eventMax')
                visitMin = request.form.get('visitMin')
                visitMax = request.form.get('visitMax')

                containSite = request.form.get('site')


                getData = 'SELECT name, manager, OpenEveryDay from beltline.site '

                cursor.execute(getData)
                info = cursor.fetchall()

                print(info)
                return render_template('site/manage_site.html', sites = sites, managers = managers, names = info)
        except Exception as e:
            print(e)
            return 'bad1'
    else:
        try:
            with conn.cursor() as cursor:
                getAllSites = 'SELECT name from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()
                print(sites)

                getAllManagers = '(SELECT username as name from manager join user using(Username) '\
                                    'where username in '\
                                    '(Select username from beltline.site join manager on manager.Username = site.Manager))'
                cursor.execute(getAllManagers)
                managers = cursor.fetchall()
                print(managers)

                getData = 'SELECT name, manager, OpenEveryDay from beltline.site '

                cursor.execute(getData)
                info = cursor.fetchall()

                print('GET')
                return render_template('site/manage_site.html', sites = sites, managers = managers, names = info)
        except Exception as e:
            print(e)
            return 'bad2'

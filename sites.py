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
            drop_down["is_selected"] = 1

            manager_info.append(drop_down)
            return render_template('site/edit_site.html', data=siteinfo, managers=manager_info)
    else:
        print("pull")
        zip_code = request.form.get('zipcode')
        address = request.form.get('address')
        manager = request.form.get('manager')
        openEveryday = request.form.get('openEveryday')
        name = SiteName
        with conn.cursor() as cursor:
            manager_username = "SELECT username AS Name1 from Manager join user using(Username) where concat(FirstName, ' ', LastName) = %s"
            cursor.execute(manager_username, (manager,))
            manager_username = cursor.fetchone()
            
            site_query = "SELECT * FROM Site WHERE Name = %s"
            cursor.execute(site_query, (SiteName))
            sites = cursor.fetchone()

            manager_username = manager_username['Name1']
            print(manager_username)
            edit_site = 'UPDATE beltline.site set `Address` = %s, ' \
            'Manager = %s, Zipcode = %s, OpenEveryDay = %s WHERE site.Name = %s'
            cursor.execute(edit_site, (ifnull(address, sites["Address"]), ifnull(manager_username, sites["Manager"]), ifnull(zip_code, sites["Zipcode"]), ifnull(openEveryday, sites["OpenEveryDay"]), name))
            conn.commit()

    return redirect('/site/edit/' + SiteName)

@bp.route('/delete/<SiteName>', methods=['GET',])
def delete(SiteName):
    conn = db.get_connection()
    with conn.cursor() as cursor:
        deleteSite = 'delete from site where name = %s'
        cursor.execute(deleteSite, SiteName)
        conn.commit()
        return redirect('/site/manage_site')


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
        newzip = request.form.get('zipcode')
        newaddress = request.form.get('address')
        newmanager = request.form.get('manager')
        newopen = request.form.get('type')
        print(newmanager)
        print('hi')
        with conn.cursor() as cursor:
            manager_username = "SELECT username AS Name1 from manager join user using(Username) where concat(FirstName, ' ', LastName) = %s"
            cursor.execute(manager_username, (newmanager))
            manager_username = cursor.fetchone()
            newmanager1 = manager_username['Name1']

            edit_site = "INSERT into beltline.site values(%s, %s, %s, %s, %s)"
            cursor.execute(edit_site, (newname, newaddress, newzip, newopen, newmanager1))
            conn.commit()

        return redirect('/site/create')
    
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

                getAllManagers = '(SELECT concat(user.FirstName," ",user.LastName) as name from manager join user using(Username) '\
                                    'where username in '\
                                    '(Select username from beltline.site join manager on manager.Username = site.Manager))'
                cursor.execute(getAllManagers)
                managers = cursor.fetchall()

                containSite = request.form.get('site')
                selectedManager = request.form.get('manager')
                print(selectedManager)
                openeveryDay = request.form.get('type')
                print(openeveryDay)

                getData = 'SELECT name,concat(user.FirstName," ",user.LastName) as manager, OpenEveryDay from beltline.site join user on site.manager = user.username ' \
                            'WHERE name like %s AND concat(user.FirstName," ",user.LastName) like %s AND OpenEveryDay like %s'

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

                getAllManagers = '(SELECT concat(user.FirstName," ",user.LastName) as name from manager join user using(Username) '\
                                    'where username in '\
                                    '(Select username from beltline.site join manager on manager.Username = site.Manager))'
                cursor.execute(getAllManagers)
                managers = cursor.fetchall()
                print(managers)

                getData = 'SELECT name,concat(user.FirstName," ",user.LastName) as manager, OpenEveryDay from beltline.site join user on site.manager = user.username '

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
            "event.StartDate between %s AND '2100-02-09' AND event.EndDate between '2001-02-09' AND %s "\
            "GROUP BY Event.SiteName, VisitEventDate, event.StartDate"


            cursor.execute(query, (startdate, enddate))
            data = cursor.fetchall()

            return render_template('details/daily_detail.html',data=data)

#36
@bp.route('/transitdetail/<SiteName>/<TransitType>', methods=['GET'])
def transit_detail(SiteName, TransitType):
    conn = db.get_connection()
    if request.method == 'GET':
        return render_template('transit/transit_detail.html')

    else:

            sitename = "Inman Park"
            transittype = "Bus"


            cursor.execute(query (sitename, transittype))
            data = cursor.fetchall()

            return render_template('transit/transit_detail.html', transit=data)

 #35

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
                oed = request.form.get('type')
                containSite = request.form.get('site')


                getData = 'Select G.SiteName, G.eventcount, F.TotalVisits, F.MyVisits from   '\
                            '(SELECT site.Name as SiteName, count(*) as eventcount  FROM beltline.site JOIN event on    '\
                            'site.name = event.SiteName group by(site.Name)) AS G   '\
                            'JOIN   '\
                            '(   '\
                            'Select C.SiteName, C.visit1 as `TotalVisits` , D.visit2 as `MyVisits` from   '\
                            '(Select A.SiteName, (A.visits + B.visits) as visit1 from   '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_site    '\
                            'WHERE `Date` BETWEEN %s AND %s   '\
                            'GROUP BY(SiteName)) as A   '\
                            'join   '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_event    '\
                            'WHERE `VisitEventDate` BETWEEN %s AND %s   '\
                            'GROUP BY(SiteName))   '\
                            'AS B    '\
                            'on A.SiteName = B.SiteName   '\
                            'Group By (A.SiteName))   '\
                            'AS C   '\
                            'Join   '\
                            '(Select A1.SiteName, (A1.visits + B1.visits) as visit2 from   '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_site     '\
                            'WHERE Username = %s AND `Date` BETWEEN %s AND %s   '\
                            'GROUP BY(SiteName)) AS A1   '\
                            'join   '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_event     '\
                            'WHERE Username = %s AND `VisitEventDate` BETWEEN %s AND %s   '\
                            'GROUP BY(SiteName)) AS B1   '\
                            'ON A1.Username = B1.Username   '\
                            'Group By (SiteName))   '\
                            'AS D   '\
                            'ON C.SiteName = D.SiteName   '\
                            ')   '\
                            'AS F   '\
                            'ON   '\
                            'G.SiteName = F.SiteName   '\
                            'WHERE G.SiteName like %s AND (F.TotalVisits BETWEEN %s AND %s) AND (G.eventcount BETWEEN %s  AND %s)   '\


                #(ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"), ifnull(oed,"%"), ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"), ifnull(oed,"%"), ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"), ifnull(oed,"%"), ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"), ifnull(oed,"%"), ifnull(containSite,"%"), ifnull(visitMin, "%"), ifnull(visitMax, "%"), ifnull(eventMin, "%"), ifnull(eventMax,"%"))
                cursor.execute(getData,(ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"),ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"),"mary.smith",ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"),"mary.smith",ifnull(startDate, "2000-01-01"), ifnull(endDate,"2040-01-01"),ifnull(containSite,"%"), ifnull(visitMin, "0"), ifnull(visitMax, "10000"), ifnull(eventMin, "0"), ifnull(eventMax,"1000")))
                #cursor.execute(getData)
                info = cursor.fetchall()

                print(info)
                return render_template('site/explore_site.html', sites = sites, siteDB = info)
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

                getData = 'Select G.SiteName, G.eventcount, F.TotalVisits, F.MyVisits from '\
                            '(SELECT site.Name as SiteName, count(*) as eventcount  FROM beltline.site JOIN event on  '\
                            'site.name = event.SiteName group by(site.Name)) AS G '\
                            'JOIN '\
                            '( '\
                            'Select C.SiteName, C.visit1 as `TotalVisits` , D.visit2 as `MyVisits` from '\
                            '(Select A.SiteName, (A.visits + B.visits) as visit1 from '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_site  '\
                            'GROUP BY(SiteName)) as A '\
                            'join '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_event  '\
                            'GROUP BY(SiteName)) '\
                            'AS B  '\
                            'on A.Username = B.Username '\
                            'Group By (A.SiteName)) '\
                            'AS C '\
                            'Join '\
                            '(Select A1.SiteName, (A1.visits + B1.visits) as visit2 from '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_site   '\
                            'WHERE Username = "mary.smith" '\
                            'GROUP BY(SiteName)) AS A1 '\
                            'join '\
                            '(SELECT Username, SiteName, count(Username) as visits FROM visit_event   '\
                            'WHERE Username = "mary.smith" '\
                            'GROUP BY(SiteName)) AS B1 '\
                            'ON A1.Username = B1.Username '\
                            'Group By (SiteName)) '\
                            'AS D '\
                            'ON C.SiteName = D.SiteName '\
                            ') '\
                            'AS F '\
                            'ON '\
                            'G.SiteName = F.SiteName'

                cursor.execute(getData)
                info = cursor.fetchall()
                print(info)
                print('GET')
                return render_template('site/explore_site.html', sites = sites, siteDB = info)
        except Exception as e:
            print(e)
            return 'bad2'

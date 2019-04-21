import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

def ifnull(var,value):
    if var == '' or var is None:
        return value
    else:
        return var.replace("'", "")

bp = Blueprint('sites', __name__, url_prefix='/site')

@bp.route('/detail/<Name>', methods=['GET'])
def detail(Name):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getALLSITES = "SELECT Name as site, OpenEveryDay as openEveryday, concat(Address, " ", Zipcode) as address FROM beltline.site"
            cursor.execute(getALLSITES)
            sites = cursor.fetchone()
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

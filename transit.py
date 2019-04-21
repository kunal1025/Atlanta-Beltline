import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('transit', __name__, url_prefix='/transit')

def ifnull(var,value):
    if var == '' or var is None:
        return value
    else:
        return var.replace("'", "")

@bp.route('/take', methods=('GET', 'POST'))
def take():
    conn = db.get_connection()
    error = None
    if request.method == 'GET':
        site = request.args.get('site')
        transport_type = request.args.get('type')
        low_price = request.args.get('lowPrice')
        high_price = request.args.get('highPrice')
        transitSQL = 'SELECT t.transitType as TransitType, t.transitRoute as TransitRoute, t.Price, count(*) as cs from transit t join connect c on t.TransitType = c.TransitType AND t.TransitRoute = c.TransitRoute ' \
                        'WHERE c.SiteName like %s AND t.transitType like %s AND (t.Price BETWEEN %s AND %s) ' \
                        'group by t.TransitType, t.TransitRoute' \

        siteSQL = "SELECT name FROM site"
        with conn.cursor() as cursor:
            cursor.execute(transitSQL, (ifnull(site, "%"), ifnull(transport_type, "%"), ifnull(low_price, 0), ifnull(high_price, 100000)))
            transits = cursor.fetchall()
            cursor.execute(siteSQL)
            sites = cursor.fetchall()
        return render_template('/transit/takeTransit.html', transits=transits, sites=sites)
    elif request.method == 'POST':
        username = session['username']
        transit = request.form.get('transit').split(',')
        date = request.form.get('date')
        take_transit = 'SELECT username from take where username = %s AND TransitDate = %s AND TransitRoute = %s AND TransitType = %s'
        with conn.cursor() as cursor:
            cursor.execute(take_transit, (username, date, transit[0], transit[1]))
            result = cursor.fetchone()
            if (result):
                error = 'You have already taken this transit today'
                flash(error)
                siteSQL = "SELECT name FROM site"
                cursor.execute(siteSQL)
                sites = cursor.fetchall()
                return render_template('/transit/takeTransit.html', sites=sites)
            else:
                takeSQL = 'INSERT INTO beltline.take values (%s, %s, %s, %s)'
                cursor.execute(takeSQL, (username, transit[1], transit[0], date))
                conn.commit()
                return redirect('/transit/take')
        return redirect('/transit/take')

@bp.route('/history', methods=('GET', 'POST'))
def history():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getSites = siteSQL = 'SELECT name FROM site'
            transitsSQL ='SELECT TransitDate as date, TransitType as type, TransitRoute as route, Price as price FROM beltline.take JOIN beltline.transit ' \
                            'USING(TransitType, TransitRoute) JOIN connect using (TransitType, TransitRoute) '\
                            'WHERE take.Username like "mary.smith" Group BY date, type, route'

            cursor.execute(getSites)
            sites = cursor.fetchall()
            cursor.execute(transitsSQL)
            transits = cursor.fetchall()
            print(transits)
            return render_template('/transit/transit_history.html', sites=sites, history = transits)
    else:
        with conn.cursor() as cursor:
            transitType = request.form.get('type')
            route = request.form.get('route')
            site = request.form.get('site')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')

            gethistory = 'SELECT TransitDate as date, TransitType as type, TransitRoute as route, Price as price FROM beltline.take JOIN beltline.transit '\
            'USING(TransitType, TransitRoute) JOIN connect using (TransitType, TransitRoute) '\
            'WHERE (%s in (Select SiteName from connect WHERE TransitRoute like %s AND TransitType like %s)) AND take.Username = "mary.smith"' \
            'AND TransitType like %s ' \
            'Group by date, type, route'
            #'WHERE (TransitDate BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE)) AND '\
            #cursor.execute(gethistory, (ifnull(start_date, '01-01-01'), ifnull(end_date, '01-01-20'), ifnull(site,'Null'), ifnull(route,"%"), ifnull(transitType,"%")))
            cursor.execute(gethistory, (ifnull(site,'Null'), ifnull(route,"%"), ifnull(transitType,"%"), ifnull(transitType,"%")))
            history = cursor.fetchall()
            print(site)
            print(transitType)
            getSites = siteSQL = 'SELECT name from site'
            cursor.execute(getSites)
            sites = cursor.fetchall()
            return render_template('/transit/transit_history.html', history=history, sites=sites)



@bp.route('/create', methods=('GET', 'POST'))
def create():
    conn = db.get_connection()
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                getSites = 'SELECT name as siteName from site'
                cursor.execute(getSites)
                sites = cursor.fetchall()
                # print(sites)
                return render_template('transit/create_transit.html', sites=sites)
        except Exception as e:
            print(e)
            return redirect('/')
            # return render_template('/error/500.html')
    else:
        transportType = request.form.get('type')
        route = request.form.get('route')
        price = request.form.get('price')
        sites = request.form.getlist('sites')

        print(transportType)
        print(route)
        print(price)
        print(sites)
        with conn.cursor() as cursor:
                insertTransit = 'Insert into transit Values (%s, %s, %s)'
                print(insertTransit)
                cursor.execute(insertTransit,(transportType, route, price))
                conn.commit()
                for site in sites:
                    insertConnect = 'Insert into connect    Values (%s, %s, %s)'
                    cursor.execute(insertConnect,(transportType, route, site))
                    conn.commit()
                sites = cursor.fetchall()
                # print(sites)
        return redirect('/transit/create')

@bp.route('/edit/<transitType>/<route>', methods=('GET', 'POST'))
def edit(transitType, route):
    conn = db.get_connection()
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                getAllSites = 'SELECT name as siteName from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()
                getSelectedSites = 'SELECT SiteName as siteName from beltline.transit join beltline.connect using(TransitType, TransitRoute) WHERE TransitRoute = %s AND TransitType = %s AND Price = price'
                cursor.execute(getSelectedSites, (route, transitType))
                selectedSites = cursor.fetchall()
                sitesList = []
                for site in selectedSites:
                    sitesList.append(site['siteName'])
                for site in sites:
                    if site['siteName'] in sitesList:
                        site['checked'] = 1
                    else:
                        site['checked'] = 0
                getTransit = 'SELECT transitType, transitRoute as route, price from transit where transitType = %s AND transitRoute = %s'
                cursor.execute(getTransit, (transitType, route))
                transit = cursor.fetchone()
                print(selectedSites)
                return render_template('transit/edit_transit.html', sites=sites, data=transit)
        except Exception as e:
            print(e)
            return redirect('/')
            # return render_template('/error/500.html')
    else:
        transitType = request.form.get('type')
        route = request.form.get('route')
        price = request.form.get('price')
        sites = request.form.getlist('sites')
        with conn.cursor() as cursor:
                alterPrice = 'Update transit set Price = %s WHERE transit.TransitType like %s AND transit.TransitRoute like %s'
                cursor.execute(alterPrice,(price, transitType, route))
                conn.commit()

                removeConnect = 'Delete from connect  WHERE TransitType = %s AND TransitRoute = %s'
                cursor.execute(removeConnect,(transitType, route))
                conn.commit()
                for site in sites:
                    insertConnect = 'Insert into connect Values (%s, %s, %s)'
                    cursor.execute(insertConnect,(transitType, route, site))
                    conn.commit()
        return redirect('/transit/edit/' + transitType + '/' + route)

@bp.route('/manage', methods=('GET', 'POST'))
def manage():
    conn = db.get_connection()
    if request.method == 'POST':
        try:
            with conn.cursor() as cursor:
                transportType = request.form.get('type')
                route = request.form.get("route")
                containSite = request.form.get('site')
                priceLow = request.form.get('lowPrice')
                priceHigh = request.form.get('highPrice')

                getSites = 'select name as siteName from site'
                cursor.execute(getSites)
                sites = cursor.fetchall()

                getTableInfo = '(SELECT TransitType as transportType, TransitRoute as route, Count(Distinct(SiteName)) as numConnectedSites, ' \
                               'count(Distinct(username)) as numTransitLogged, Price as price from connect join transit using(TransitType, TransitRoute) ' \
                               'join take using(TransitType, TransitRoute) WHERE TransitType like %s AND TransitRoute like %s ' \
                               'AND  SiteName like %s AND Price between %s AND %s ' \
                               'group by TransitType, TransitRoute) ' \
                               'UNION ' \
                               '(SELECT TransitType, TransitRoute, Count(Distinct(SiteName)) AS "# Connected Sites","0" as numConnectedSites, Price from connect '\
                                'join transit using(TransitType, TransitRoute) '\
                                'WHERE NOT concat(TransitType, TransitRoute) in (Select concat(TransitType, TransitRoute) from take) '\
                                'AND TransitType like %s AND TransitRoute like %s AND  SiteName like %s AND Price between %s AND %s ' \
                                'group by concat(TransitType, TransitRoute))'

                cursor.execute(getTableInfo, (ifnull(transportType,"%"), ifnull(route, "%"), ifnull(containSite, "%"), ifnull(priceLow, 0), ifnull(priceHigh, 100000), ifnull(transportType,"%"), ifnull(route, "%"), ifnull(containSite, "%"), ifnull(priceLow, 0), ifnull(priceHigh, 100000)))
                info = cursor.fetchall()
                print(transportType)
                print('help')

                return render_template('transit/manage_transit.html', sites=sites, routes=info)
        except Exception as e:
            print(e)
    else:
        try:
            with conn.cursor() as cursor:
                getSites = 'select name as siteName from site'
                cursor.execute(getSites)
                sites = cursor.fetchall()
                getTableInfo = '(SELECT TransitType as transportType, TransitRoute as route, Count(Distinct(SiteName)) as numConnectedSites, ' \
                               'count(Distinct(username)) as numTransitLogged, Price as price from connect join transit using(TransitType, TransitRoute) ' \
                               'join take using(TransitType, TransitRoute) ' \
                               'group by TransitType, TransitRoute) ' \
                               'UNION ' \
                               '(SELECT TransitType, TransitRoute, Count(Distinct(SiteName)) AS "# Connected Sites","0" as numConnectedSites, Price from connect '\
                                'join transit using(TransitType, TransitRoute) '\
                                'WHERE NOT concat(TransitType, TransitRoute) in (Select concat(TransitType, TransitRoute) from take) '\
                                'group by concat(TransitType, TransitRoute))'

                cursor.execute(getTableInfo)
                info = cursor.fetchall()
                # getTableInfo = 'SELECT TransitType as transportType, TransitRoute as route, Count(Distinct(SiteName)) as numConnectedSites, ' \
                #                'count(Distinct(username)) as numTransitLogged, Price as price from connect join transit using(TransitType, TransitRoute)' \
                #                'join take using(TransitType, TransitRoute) group by concat(TransitType, TransitRoute)'
                # cursor.execute(getTableInfo)
                # info = cursor.fetchall()

                return render_template('transit/manage_transit.html', sites=sites, routes=info)
        except Exception as e:
            print(e)

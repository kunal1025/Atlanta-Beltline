import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('transit', __name__, url_prefix='/transit')

@bp.route('/take', methods=('GET', 'POST'))
def take():
    conn = db.get_connection()
    error = None
    if request.method == 'GET':
        site = request.args.get('site')
        transport_type = request.args.get('type')
        low_price = request.args.get('lowPrice')
        high_price = request.args.get('highPrice')
        transitSQL = 'select t.transitType as TransitType, t.transitRoute as TransitRoute, t.Price, count(*) as cs from transit t join connect c where t.TransitType = c.TransitType AND t.TransitRoute = c.TransitRoute group by t.TransitType, t.TransitRoute'
        siteSQL = 'select name from site'
        with conn.cursor() as cursor:
            cursor.execute(transitSQL)
            transits = cursor.fetchall()
            cursor.execute(siteSQL)
            sites = cursor.fetchall()
        return render_template('/transit/takeTransit.html', transits=transits, sites=sites)
    elif request.method == 'POST':
        username = session['username']
        transit = request.form.get('transit').split(',')
        date = request.form.get('date')
        take_transit = 'select username from take where username = %s AND TransitDate = %s AND TransitRoute = %s AND TransitType = %s'
        with conn.cursor() as cursor:
            cursor.execute(take_transit, (username, date, transit[0], transit[1]))
            result = cursor.fetchone()
            if (result):
                error = 'You have already taken this transit today'
                flash(error)
                return render_template('/transit/take')
            else:
                #TODO: write query to insert to take
                return redirect('/transit/take')
        return redirect('/transit/take')

@bp.route('/history', methods=('GET', 'POST'))
def history():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            getSites = siteSQL = 'select name from site'
            cursor.execute(getSites)
            sites = cursor.fetchall()
            return render_template('/transit/transit_history.html', sites=sites)
    else:
        with conn.cursor() as cursor:
            transitType = request.form.get('type')
            route = request.form.get('route')
            site = request.form.getlist('site')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')

            gethistory = 'SELECT TransitDate, TransitType, TransitRoute, Price FROM beltline.take JOIN beltline.transit ' \
            'USING(TransitType, TransitRoute) WHERE (TransitDate BETWEEN %s AND %s) AND SiteName = %s AND ' \
            'TransitRoute = %s AND TransitType = %s'
            cursor.execute(gethistory, (start_date, end_date, site, route, transitType))
            history = cursor.fetchall()

            getSites = siteSQL = 'select name from site'
            cursor.execute(getSites)
            sites = cursor.fetchall()
            return render_template('/transit/transit_history.html', history=history, sites=sites)



@bp.route('/create', methods=('GET', 'POST'))
def create():
    conn = db.get_connection()
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                getSites = 'select name as siteName from site'
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

        # print(transportType)
        # print(route)
        # print(price)
        # print(sites)
        #
        return redirect('/transit/create')

@bp.route('/edit/<transitType>/<route>', methods=('GET', 'POST'))
def edit(transitType, route):
    conn = db.get_connection()
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                getAllSites = 'select name as siteName from site'
                cursor.execute(getAllSites)
                sites = cursor.fetchall()
                getSelectedSites = 'select SiteName as siteName from beltline.transit join beltline.connect using(TransitType, TransitRoute) ' \
                           'where TransitRoute = %s AND TransitType = %s AND Price = price'
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
                getTransit = 'select transitType, transitRoute as route, price from transit where transitType = %s AND transitRoute = %s'
                cursor.execute(getTransit, (transitType, route))
                transit = cursor.fetchone()
                print(selectedSites)
                return render_template('transit/edit_transit.html', sites=sites, data=transit)
        except Exception as e:
            print(e)
            return redirect('/')
            # return render_template('/error/500.html')
    else:
        transportType = request.form.get('type')
        route = request.form.get('route')
        price = request.form.get('price')
        sites = request.form.getlist('sites')

        # print(tranportType)
        # print(route)
        # print(price)
        # print(sites)
        #
        return redirect('/transit/create')

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

                getTableInfo = 'SELECT TransitType as transportType, TransitRoute as route, Count(Distinct(SiteName)) as numConnectedSites, ' \
                               'count(Distinct(username)) as numTransitLogged, Price as price from connect join transit using(TransitType, TransitRoute)' \
                               'join take using(TransitType, TransitRoute) WHERE TransitType = %s AND TransitRoute = %s' \
                               'AND  SiteName = %s AND Price between %s AND %s' \
                               'group by concat(TransitType, TransitRoute)'
                cursor.execute(getTableInfo, (transportType, route, containSite, priceLow, priceHigh))
                info = cursor.fetchall()

                return render_template('transit/manage_transit.html', sites=sites, routes=info)
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
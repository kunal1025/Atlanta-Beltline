import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('transit', __name__, url_prefix='/transit')
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
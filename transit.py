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
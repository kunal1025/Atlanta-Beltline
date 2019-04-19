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
        tranportType = request.form.get('type')
        route = request.form.get('route')
        price = request.form.get('price')
        sites = request.form.getlist('sites')

        # print(tranportType)
        # print(route)
        # print(price)
        # print(sites)
        #
        return redirect('/transit/create')

@bp.route('/edit/<transportType>/<route>', methods=('GET', 'POST'))
def edit(transportType, route):
    conn = db.get_connection()

    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                sites = 'select name as siteName from site'
                cursor.execute(sites)
                getSites = cursor.fetchall()
                selectedSites = 'select SiteName as siteName from beltline.transit join beltline.connect using(TransitType, TransitRoute) ' \
                           'where TransitRoute = "%s" AND TransitType = "%s" AND Price = price'
                cursor.execute(selectedSites)
                getSelectedInformation = cursor.fetchall()
                new_getSite = []
                getSitesList = [i['siteName'] for i in getSites]
                getSelectedInfoList = [i['siteName'] for i in getSelectedInformation]
                for site in getSitesList:
                    if site in getSelectedInfoList:
                        x = {}
                        x['siteName'] = site
                        x['checked'] = 1
                        new_getSite.append(x)

                    else:
                        x = {}
                        x['siteName'] = site
                        x['checked'] = 0
                        new_getSite.append(x)
                print(new_getSite)
                return render_template('transit/create_transit.html', sites=sites)
        except Exception as e:
            print(e)
            return redirect('/')
            # return render_template('/error/500.html')
    else:
        tranportType = request.form.get('type')
        route = request.form.get('route')
        price = request.form.get('price')
        sites = request.form.getlist('sites')

        # print(tranportType)
        # print(route)
        # print(price)
        # print(sites)
        #
        return redirect('/transit/create')
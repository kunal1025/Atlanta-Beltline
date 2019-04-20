import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
import db

bp = Blueprint('sites', __name__, url_prefix='/site')
@bp.route('/edit/<SiteName>', methods=['GET', 'POST'])
# THE HTML IS INCORRECT
def edit(SiteName):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            siteinfo = "select Name, Address, Zipcode, Manager, OpenEveryDay from site where Name = %s"
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
            return render_template('site/edit_site.html', data=siteinfo, managers = info)
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


def create(SiteName):
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            siteinfo = "select Name, Zipcode, Manager, OpenEveryDay from site where site = %s"
            cursor.execute(siteinfo, (SiteName,))
            info = cursor.fetchone()

            manager_drop_down = "SELECT concat(FirstName," ",LastName) from manager join user using(Username)"\
            "where username not in (Select username from beltline.site join manager on manager.Username = site.Manager)"
            cursor.execute(manager_drop_down)

            return render_template('site/edit_site.html', data=info)
            

    else:
        name = request.form.get('name')
        zip_code = request.form.get("zipcode")
        address = request.form.get('address')
        manager = request.form.get('manager')
        openEveryday = request.form.get('openeveryday')
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

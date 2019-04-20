import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

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

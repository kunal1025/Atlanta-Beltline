import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
import db

def ifnull(var,value):
    if var == '' or var is None:
        return value
    else:
        return var.replace("'", "")

bp = Blueprint('visit', __name__, url_prefix='/visit')
@bp.route('/history', methods=('GET',))
def history():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            username = session["username"]
            startdate = request.form.get("startdate")
            enddate = request.form.get("enddate")
            eventname = request.form.get("event")

            visit_history = "(SELECT VisitEventDate AS date, VisitEventName AS event, Event.SiteName AS site, Price from visit_event join event ON event.Name = visit_event.VisitEventName AND event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate WHERE username = %s AND event.StartDate >= %s AND event.EndDate <= %s AND event.Name = %s) UNION (SELECT Date, '' AS VisitEventName, Name AS SiteName, '0' AS Price from site join visit_site on visit_site.SiteName = site.Name WHERE username = %s)"

            cursor.execute(visit_history, (username, ifnull(startdate, "%"), ifnull(enddate, "%"), ifnull(eventname, "%"), username))
            visit_history = cursor.fetchall()

            sites_query = "SELECT site.Name AS site from beltline.site"
            cursor.execute(sites_query)
            sites = cursor.fetchall()

        return render_template('visit_history.html', data=visit_history, sites=sites)
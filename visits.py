import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
import db
bp = Blueprint('transit', __name__, url_prefix='/visit')
@bp.route('/edit/<SiteName>', methods=['GET', 'POST'])
def history():
    conn = db.get_connection()
    if request.method == 'GET':
        with conn.cursor() as cursor:
            visit_history = "(SELECT VisitEventDate AS date, VisitEventName AS event, Event.SiteName AS site, Price from visit_event join event "\
            "ON event.Name = visit_event.VisitEventName AND event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate WHERE username = %s) "\
            "UNION (SELECT Date, "" AS VisitEventName, Name AS SiteName, "0" AS Price from site join visit_site on visit_site.SiteName = site.Name) "\
            "WHERE username = %s"
            cursor.execute(visit_history, )

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp.route('/view', methods=('GET', 'POST'))
def view():
	conn = db.get_connection()
	if request.method == 'GET':
		return render_template("/view_schedule.html")
	else:
		# try:
			with conn.cursor() as cursor:
				eventName = request.form.get('eventName')
				description = request.form.get('desc')
				desc = "%" + description + "%"
				startDate = request.form.get('startDate')
				endDate = request.form.get('endDate')

				getEvent = 'SELECT Name as eventName, SiteName as siteName, event.StartDate as startDate, event.EndDate as endDate, ' \
						  'count(Username) from event JOIN assign_to using(eventName, siteName) WHERE event.Name = %s' \
						  'AND event.StartDate between %s AND "2100-02-09" AND event.EndDate ' \
						  'between "2001-02-09" AND %s AND event.description LIKE %s ' \
						  'GROUP BY event.StartDate, Name, SiteName'


				cursor.execute(getEvent, (eventName, startDate, endDate, desc))
				event = cursor.fetchall()

				return render_template('/view_schedule.html', events=event)
		# except Exception as e:
		# 	print(e)
		# 	print("exception")
		# return redirect('/')
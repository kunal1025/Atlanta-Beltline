import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

def ifnull(var,value):
    if var == '' or var is None:
        return value
    else:
        return var.replace("'", "")


@bp.route('/view', methods=('GET', 'POST'))
def view():
	conn = db.get_connection()
	if request.method == 'GET':
		with conn.cursor() as cursor:
			getEvent = 'SELECT Name as eventName, SiteName as siteName, event.StartDate as startDate, event.EndDate as endDate, count(Username) as staffCount from '\
						'event JOIN assign_to using(Name, SiteName) '\
						'GROUP BY event.StartDate, Name, SiteName '
			cursor.execute(getEvent)
			event = cursor.fetchall()

		return render_template("/view_schedule.html", events=event)
	else:
		# try:
			with conn.cursor() as cursor:
				eventName = request.form.get('eventName')
				description = request.form.get('desc')
				desc = "%" + description + "%"
				startDate = request.form.get('startDate')
				endDate = request.form.get('endDate')

				getEvent = 'SELECT Name as eventName, SiteName as siteName, event.StartDate as startDate, event.EndDate as endDate, count(Username) as staffCount from '\
						'event JOIN assign_to using(Name, SiteName) WHERE Name like %s AND event.description like %s '\
						'AND event.StartDate between %s AND "2100-02-09" AND event.EndDate between "2001-02-09" AND %s '\
						'GROUP BY event.StartDate, Name, SiteName '
							#'event.description LIKE %s ' \

				#cursor.execute(getEvent, (ifnull(eventName,"%"), ifnull(startDate,"2000-01-01"), ifnull(endDate,"2100-02-09"), ifnull(desc,"%")))
				cursor.execute(getEvent, (ifnull(eventName,"%"), ifnull(desc,"%"), ifnull(startDate,"2000-01-01"), ifnull(endDate,"2100-02-09")))
				event = cursor.fetchall()

				return render_template('/view_schedule.html', events=event)
		# except Exception as e:
		# 	print(e)
		# 	print("exception")
		# return redirect('/')

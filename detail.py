import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('detail', __name__, url_prefix='/detail')

@bp.route('/daily/<startDate>/<endDate>/<visitDate>', methods=('GET', 'POST'))
def daily(startDate, endDate, visitDate):
	conn = db.get_connection()
	if request.method == 'GET':
		try:
			with conn.cursor() as cursor:
				# startDate = request.args.get('startDate')
				# endDate = request.args.get('staffName')
				# siteName = request.args.get('siteName')
				# visitDate = request.args.get('visitDate')
				# startDate = request.args.get('startDate')
				visits = request.args.get('visits')
				revenue = request.args.get('revenue')

				getName = 'SELECT VisitEventName, count(Username) AS Visit, price, price*count(Username) AS' \
						  'Revenue FROM event JOIN visit_event ON event.Name = visit_event.VisitEventName AND ' \
						  'event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate WHERE ' \
						  'StartDate >= %s AND EndDate <= %s' \
						  'GROUP BY concat(Event.SiteName, VisitEventDate as %s, event.StartDate as %s)'
				cursor.execute(getName, (startDate, endDate, visitDate, startDate))
				names = cursor.fetchall()

				return render_template('/detail/daily_detail.html', dataDB=names)
		except Exception as e:
			print(e)
			print("exception")
			return redirect('/')
	else:
		print("running from the else block")
		return redirect('/')
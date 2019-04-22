import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('detail', __name__, url_prefix='/detail')

@bp.route('/daily/<date>', methods=('GET',))
def daily(date):
	conn = db.get_connection()
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
						'visit_event.VisitEventDate = %s' \
						'GROUP BY concat(Event.SiteName, VisitEventDate, event.StartDate)'
			cursor.execute(getName, (date))
			names = cursor.fetchall()
			print(names)
			return render_template('/detail/daily_detail.html', sites=names)
	except Exception as e:
		print(e)
		print("exception")
		# return redirect('/')

#30
@bp.route('/dailydetail/<date>', methods=['GET'])
def daily_detail(date):
	conn = db.get_connection()
	if request.method == 'GET':
		with conn.cursor() as cursor:
			sitename = session["site"]
			# print(sitename)

			query = "SELECT VisitEventName AS eventName, group_concat(Distinct concat(User.FirstName, ' ', User.LastName)) as staffNames, " \
            "count(visit_event.Username) AS visits, Price, Price*count(visit_event.Username) as " \
            "revenue from event join visit_event on event.Name = visit_event.VisitEventName AND " \
            "event.SiteName = visit_event.SiteName AND event.StartDate = visit_event.StartDate JOIN " \
            "assign_to ON assign_to.Name = event.Name AND assign_to.SiteName = event.SiteName AND " \
            "assign_to.StartDate = event.StartDate JOIN user on user.Username = assign_to.Username " \
            "WHERE visit_event.VisitEventDate = %s AND visit_event.SiteName = %s " \
            "group by event.SiteName, visit_event.VisitEventDate, event.StartDate"

			cursor.execute(query, (date))
			data = cursor.fetchall()
			print(data)
			return render_template('details/daily_detail.html',dataDB=data)

# 32
@bp.route('/staffeventdetail/<SiteName>/<Name>/<StartDate>', methods=('GET',))
def event_detail(SiteName, Name, StartDate):
    conn = db.get_connection()
    with conn.cursor() as cursor:
        query = "Select FirstName, LastName, group_concat(FirstName, LastName) AS staffName,Name AS eventName, " \
        "SiteName AS siteName, StartDate as startDate, EndDate AS endDate, capacity, datediff(EndDate, StartDate) " \
        "as durationDays, price, description as `desc` FROM assign_to JOIN user using (Username) JOIN event using" \
        "(SiteName, Name, StartDate) WHERE assign_to.SiteName = %s AND assign_to.StartDate = %s AND assign_to.Name = %s"
        
        cursor.execute(query, (SiteName, StartDate, Name))
        data = cursor.fetchone()
        print(data)
        return render_template('details/staff_event_detail.html',event=data)
 

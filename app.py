from flask import Flask
from flask import render_template, redirect, session, request
import auth
import db

app = Flask(__name__)
app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev')

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/transit', methods=['GET', 'POST'])
def takeTransit():
    conn = db.get_connection()
    error = None
    if request.method == 'GET':
        site = request.args.get('site')
        transport_type = request.args.get('type')
        low_price = request.args.get('lowPrice')
        high_price = request.args.get('highPrice')
        transitSQL = 'select t.transitType as TransitType, t.transitRoute as TransitRoute, t.Price, count(*) as cs from transit t join connect c where t.TransitType = c.TransitType AND t.TransitRoute = c.TransitRoute group by t.TransitType, t.TransitRoute'
        siteSQL = 'select name from site'
        with conn.cursor() as cursor:
            cursor.execute(transitSQL)
            transits = cursor.fetchall()
            cursor.execute(siteSQL)
            sites = cursor.fetchall()
        return render_template('/auth/takeTransit.html', transits=transits, sites=sites)
    elif request.method == 'POST':
        username = session['username']
        transit = request.form.get('transit').split(',')
        date = request.form.get('date')
        take_transit = 'select username from take where username = %s AND TransitDate = %s AND TransitRoute = %s AND TransitType = %s'
        print(transit[0])
        print(transit[1])
        with conn.cursor() as cursor:
            cursor.execute(take_transit, (username, date, transit[0], transit[1]))
            result = cursor.fetchone()
            if (result):
                return redirect('/transit')
            else:
                #insert into table
                return redirect('/transit')
        return redirect('/transit')

app.register_blueprint(auth.bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
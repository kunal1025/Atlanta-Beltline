from flask import Flask
from flask import render_template, redirect
import auth
import db

app = Flask(__name__)
app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev')

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/transit', methods=['GET'])
def takeTransit():
    conn = db.get_connection()
    sql = 'select * from transit'
    with conn.cursor() as cursor:
        cursor.execute(sql)
        transits = cursor.fetchall()
        print(transits)
    return render_template('/auth/takeTransit.html', transits=transits)

app.register_blueprint(auth.bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
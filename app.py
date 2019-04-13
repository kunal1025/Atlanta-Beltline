from flask import Flask
from flask import render_template, redirect
import auth

app = Flask(__name__)
app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev')

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

app.register_blueprint(auth.bp)

# a simple page that says hello
@app.route('/hello', methods=['GET'])
def hello():
    result = 'hello world'
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'select * from user'
            cursor.execute(sql)
            result = cursor.fetchone()
    except Exception as e:
        print(e)
    return result['Username']
    #return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
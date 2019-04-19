from flask import Flask
from flask import render_template, redirect, session, request
import auth, register, transit
import db

app = Flask(__name__)
app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev')

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

app.register_blueprint(auth.bp)
app.register_blueprint(register.bp)
app.register_blueprint(transit.bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask
from flask import render_template, redirect, session, request
import auth, register, transit, sites, event, detail, visit, schedule
import db

app = Flask(__name__)
app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev')

@app.route('/', methods=['GET'])
def home_page():
    role = session.get('role', None)
    if (not role):
        return render_template('index.html')
    elif (role == 'admin'):
        return render_template('/functionality/admin_only_functionality.html')
    elif (role == 'admin-visitor'):
        return render_template('/functionality/admin_visitor_functionality.html')
    elif (role == 'manager'):
        return render_template('/functionality/manager_only_functionality.html')
    elif (role == 'manager-visitor'):
        return render_template('/functionality/manager_visitor_functionality.html')
    elif (role == 'staff'):
        return render_template('/functionality/staff_only_functionality.html')
    elif (role == 'staff-visitor'):
        return render_template('/functionality/staff_visitor_functionality.html')
    elif (role == 'visitor'):
        return render_template('/functionality/visitor_functionality.html')
    else:
        return render_template('/functionality/user_functionality.html')

app.register_blueprint(auth.bp)
app.register_blueprint(register.bp)
app.register_blueprint(transit.bp)
app.register_blueprint(sites.bp)
app.register_blueprint(event.bp)
app.register_blueprint(detail.bp)
app.register_blueprint(visit.bp)
app.register_blueprint(schedule.bp)
app.register_blueprint(manage.bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

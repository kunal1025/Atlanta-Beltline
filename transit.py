import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('transit', __name__, url_prefix='/transit')

@bp.route('/login', methods=('GET', 'POST'))
def create():
    if request.method == 'GET':
        return render_template('transit/create_transit.html')
    else:

        conn = db.get_connection()

def
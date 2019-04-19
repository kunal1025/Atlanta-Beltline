import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('sites', __name__, url_prefix='/site')

@bp.route('/', methods=['GET'])
def idk():
    return redirect('/')
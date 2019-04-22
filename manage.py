import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import db

bp = Blueprint('manage', __name__, url_prefix='/manage')
from flask import Blueprint

welcome = Blueprint('welcome', __name__)

from . import views, errors

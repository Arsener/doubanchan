from flask import Blueprint

actor = Blueprint('actor', __name__)

from . import views, errors

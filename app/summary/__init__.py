from flask import Blueprint

summary = Blueprint('summary', __name__)

from . import views, errors

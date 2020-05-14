from . import search
from flask import render_template

@search.route('/')
def index():
    return render_template('welcome.html')
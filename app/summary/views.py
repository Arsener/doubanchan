from . import summary
from flask import render_template

@summary.route('/')
def index():
    return render_template('welcome.html')
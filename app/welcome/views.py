from . import welcome
from flask import Flask, render_template

@welcome.route('/')
def index():
    return render_template('welcome.html')
#!/usr/bin/env python
import os
from app import create_app
import pymysql
from config import *
from flask_cors import CORS

db = None
database_name = DB
try:
    db = pymysql.connect('localhost', 'root', PWD, database_name, charset='utf8')
except:
    db = pymysql.connect('166.111.83.75', 'admin', PWD, database_name, port=3306, charset='utf8')

app = create_app('default')
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

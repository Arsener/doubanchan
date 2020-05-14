import pymysql

BACKUP_DB = 'backup_doubanchan_movie'
DB = 'doubanchan_movie'
NEW_DB = 'new_doubanchan_movie'
PWD = 'data@1234'

def get_db():
    try:
        db = pymysql.connect('localhost', 'root', PWD, DB, charset='utf8')
    except:
        db = pymysql.connect('166.111.83.75', 'admin', PWD, DB, port=3306, charset='utf8')

    return db
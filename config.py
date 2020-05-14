import os

basedir = os.path.abspath(os.path.dirname(__file__))

BACKUP_DB = 'backup_doubanchan_movie'
DB = 'doubanchan_movie'
NEW_DB = 'new_doubanchan_movie'
PWD = 'data@1234'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ihnsu2#RWE#wads'

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config,
}

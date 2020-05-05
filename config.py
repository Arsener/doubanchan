import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ihnsu2#RWE#wads'

    @staticmethod
    def init_app(app):
        pass

config = {
    'default': Config,
}


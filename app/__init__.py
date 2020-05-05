from flask import Flask
from config import config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)

    from .welcome import welcome as welcome_blueprint
    app.register_blueprint(welcome_blueprint)

    from .movie import movie as movie_blueprint
    app.register_blueprint(movie_blueprint, url_prefix='/movie')

    from .actor import actor as actor_blueprint
    app.register_blueprint(actor_blueprint, url_prefix='/actor')

    from .summary import summary as summary_blueprint
    app.register_blueprint(summary_blueprint, url_prefix='/summary')

    return app

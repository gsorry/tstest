import os
from flask import Flask
from flask import render_template
from tsapp.models import db
from tsapp.models import init_db_command
from tsapp.resources import register_blueprints


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_ECHO=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(app.instance_path, 'tsapp.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(400)
    def bad_request(e):
        app.logger.exception(e)
        return 'Bad Request', 400

    @app.errorhandler(401)
    def unauthorized(e):
        app.logger.exception(e)
        return 'Unauthorized Access', 401

    @app.errorhandler(404)
    def not_found(e):
        app.logger.exception(e)
        return 'Not Found', 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.exception(e)
        return 'Internal Server Error', 500

    @app.errorhandler(501)
    def not_implemented(e):
        app.logger.exception(e)
        return 'Not Implemented', 501

    db.init_app(app)

    app.cli.add_command(init_db_command)

    register_blueprints(app)

    return app

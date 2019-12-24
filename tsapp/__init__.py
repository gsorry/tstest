import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_ECHO=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(app.instance_path, 'tsapp.sqlite'),
        PAGINATION_PAGE_SIZE=50,
        PAGINATION_PAGE_ARGUMENT_NAME='page',
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
        return 'tsapp', 200

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

    return app

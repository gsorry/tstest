from tsapp.resources.auth import auth_blueprint
from tsapp.resources.users import users_blueprint


def register_blueprints(app):
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(users_blueprint, url_prefix='/users')

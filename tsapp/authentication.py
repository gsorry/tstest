from flask import g
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from tsapp.models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_email_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    return 'Unauthorized Access', 401


class AuthenticationRequiredResource(Resource):
    method_decorators = [auth.login_required]

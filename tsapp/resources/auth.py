from flask import Blueprint
from flask import Response
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask_restful import Api
from flask_restful import Resource

auth_blueprint = Blueprint('auth', __name__)

auth_api = Api(auth_blueprint)


class RegisterResource(Resource):
    def get(self):
        return Response(render_template('auth/register.html'), mimetype='text/html')

    def post(self):
        pass


class LoginResource(Resource):
    @auth_api.representation('text/html')
    def get(self):
        return Response(render_template('auth/login.html'), mimetype='text/html')

    def post(self):
        pass


class LogoutResource(Resource):
    def get(self):
        session.clear()
        return redirect(url_for('auth.loginresource'))


class RequestPasswordResource(Resource):
    def get(self):
        return Response(render_template('auth/request_password.html'), mimetype='text/html')

    def post(self):
        pass


class ResetPasswordResource(Resource):
    def get(self):
        return Response(render_template('auth/reset_password.html'), mimetype='text/html')

    def post(self):
        pass


auth_api.add_resource(RegisterResource, '/register/')
auth_api.add_resource(LoginResource, '/login/')
auth_api.add_resource(LogoutResource, '/logout/')
auth_api.add_resource(RequestPasswordResource, '/request_password/')
auth_api.add_resource(ResetPasswordResource, '/reset_password/')

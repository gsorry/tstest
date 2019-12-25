from flask import Blueprint
from flask_restful import Api
from tsapp.authentication import AuthenticationRequiredResource

users_blueprint = Blueprint('users', __name__)

users_api = Api(users_blueprint)


class ProfileResource(AuthenticationRequiredResource):
    def get(self):
        pass


users_api.add_resource(ProfileResource, '/profile/')

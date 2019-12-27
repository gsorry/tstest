from flask import Blueprint
from flask import Response
from flask import render_template
from flask import session
from flask_restful import Api
from tsapp.authentication import AuthenticationRequiredResource
from tsapp.models import User

users_blueprint = Blueprint('users', __name__)

users_api = Api(users_blueprint)


class ProfileResource(AuthenticationRequiredResource):
    def get(self):
        user = User.query.get_or_404(session['user_id'])
        return Response(render_template('users/profile.html', user=user), mimetype='text/html')


users_api.add_resource(ProfileResource, '/profile/')

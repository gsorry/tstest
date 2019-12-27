import functools
from flask import session
from flask import redirect
from flask import url_for
from flask_restful import Resource


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session or session['user_id'] is None:
            return redirect(url_for('auth.loginresource'))

        return view(**kwargs)

    return wrapped_view


class AuthenticationRequiredResource(Resource):
    method_decorators = [login_required]

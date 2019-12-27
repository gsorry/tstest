import base64
from flask import Blueprint
from flask import Response
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import current_app
from flask_restful import Api
from flask_restful import Resource
from sqlalchemy import exc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from tsapp.models import User
from tsapp.models import UserSchema
from tsapp.forms import UserForm
from tsapp.forms import LoginForm
from tsapp.forms import RequestPasswordForm
from tsapp.forms import ResetPasswordForm

auth_blueprint = Blueprint('auth', __name__)

auth_api = Api(auth_blueprint)

user_schema = UserSchema()


class RegisterResource(Resource):
    def get(self):
        return Response(render_template('auth/register.html'), mimetype='text/html')

    def post(self):
        user_form = UserForm(request.form)
        if user_form.validate():
            user = User(email=user_form.email.data)
            try:
                error_message, password_ok = user.check_password_strength_and_hash_if_ok(user_form.password.data)
                if password_ok:
                    user.fullname = user_form.fullname.data
                    user.add(user)
                    flash("You have successfully registered to tsapp application.")
                    return redirect(url_for('auth.loginresource'))
                else:
                    flash(error_message)
            except exc.IntegrityError:
                flash("The email address already exist. Please, specify different email address.")
        else:
            if 'email' in user_form.errors:
                flash(user_form.errors['email'][0])
            if 'password' in user_form.errors:
                flash(user_form.errors['password'][0])
            if 'fullname' in user_form.errors:
                flash(user_form.errors['fullname'][0])

        return redirect(url_for('auth.registerresource'))


class LoginResource(Resource):
    def get(self):
        return Response(render_template('auth/login.html'), mimetype='text/html')

    def post(self):
        login_form = LoginForm(request.form)
        if login_form.validate():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user is not None:
                if user.verify_password(login_form.password.data):
                    session.clear()
                    session['user_id'] = user.id
                    return redirect(url_for('users.profileresource'))
                else:
                    flash("Wrong password.")
            else:
                flash("Email address does not exist.")
        else:
            if 'email' in login_form.errors:
                flash(login_form.errors['email'][0])
            if 'password' in login_form.errors:
                flash(login_form.errors['password'][0])

        return redirect(url_for('auth.loginresource'))


class LogoutResource(Resource):
    def get(self):
        session.clear()
        return redirect(url_for('auth.loginresource'))


class RequestPasswordResource(Resource):
    def get(self):
        return Response(render_template('auth/request_password.html'), mimetype='text/html')

    def post(self):
        request_password_form = RequestPasswordForm(request.form)
        if request_password_form.validate():
            user = User.query.filter_by(email=request_password_form.email.data).first()
            if user is not None:
                token = str(base64.urlsafe_b64encode(user.email.encode("utf-8")), "utf-8")
                message = Mail(
                    from_email=current_app.config['SENDGRID_SENDER_EMAIL'],
                    to_emails=user.email,
                    subject='tsapp reset password link',
                    html_content='Please, click on the following link to reset your password:'
                                 '<a href="{link}">{link}</a>'.format(link=url_for('auth.resetpasswordresource', token=token, _external=True))
                )
                try:
                    sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
                    response = sg.send(message)
                    flash("Please, check your inbox. An email has been sent to you with instructions for resetting your password.")
                    return redirect(url_for('auth.loginresource'))
                except Exception as e:
                    flash(e.message)
            else:
                flash("This email address does not exist in our database. Please, specify different email address.")
        else:
            if 'email' in request_password_form.errors:
                flash(request_password_form.errors['email'][0])

        return redirect(url_for('auth.requestpasswordresource'))


class ResetPasswordResource(Resource):
    def get(self):
        token = request.args.get('token', '', type=str)
        email = str(base64.b64decode(token), "utf-8")
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return Response(render_template('auth/reset_password.html', token=token), mimetype='text/html')
        else:
            flash("Invalid link. Please, specify different email address.")
        return redirect(url_for('auth.requestpasswordresource'))

    def post(self):
        reset_password_form = ResetPasswordForm(request.form)
        token = reset_password_form.token.data
        if reset_password_form.validate():
            email = str(base64.b64decode(token), "utf-8")
            user = User.query.filter_by(email=email).first()
            if user is not None:
                error_message, password_ok = user.check_password_strength_and_hash_if_ok(reset_password_form.password.data)
                if password_ok:
                    user.update()
                    flash("You have successfully changed the password.")
                    return redirect(url_for('auth.loginresource'))
                else:
                    flash(error_message)
                return redirect(url_for('auth.resetpasswordresource', token=token))
            else:
                flash("Invalid link. Please, specify different email address.")
        else:
            if 'password' in reset_password_form.errors:
                flash(reset_password_form.errors['password'][0])
            if 'token' in reset_password_form.errors:
                flash("Invalid link. Please, specify different email address.")

        return redirect(url_for('auth.resetpasswordresource', token=token))


auth_api.add_resource(RegisterResource, '/register/')
auth_api.add_resource(LoginResource, '/login/')
auth_api.add_resource(LogoutResource, '/logout/')
auth_api.add_resource(RequestPasswordResource, '/request_password/')
auth_api.add_resource(ResetPasswordResource, '/reset_password/')

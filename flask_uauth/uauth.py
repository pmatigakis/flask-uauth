from werkzeug.exceptions import Unauthorized
from flask import current_app


class UAuth(object):
    def __init__(self, app=None, authentication_callback=None):
        self.app = app
        self.authentication_callback = authentication_callback

        if app is not None:
            self.init_app(
                app=app,
                authentication_callback=self.authentication_callback
            )

    @property
    def auth_header(self):
        app = self._get_app()

        return app.config.get("UAUTH_AUTHENTICATION_HEADER", "Authorization")

    @property
    def auth_argument(self):
        app = self._get_app()

        return app.config.get("UAUTH_AUTHENTICATION_ARGUMENT")

    def _get_app(self):
        return self.app or current_app

    def _handle_unauthorized_user(self):
        raise Unauthorized()

    def _handle_missing_token(self):
        raise Unauthorized()

    def init_app(self, app, authentication_callback=None):
        self.authentication_callback = (
                authentication_callback or self.authentication_callback)

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["uauth"] = self

    def get_token(self, authorization_value):
        return self.authentication_callback(authorization_value)

    def authenticate_request(self, request):
        authorization_value = None

        if self.auth_header is not None:
            authorization_value = request.headers.get(self.auth_header)

        if authorization_value is None and self.auth_argument is not None:
            authorization_value = request.args.get(self.auth_argument)

        if authorization_value is None:
            return self._handle_missing_token()

        token = self.get_token(authorization_value)
        if token is None or not token.is_active():
            return self._handle_unauthorized_user()

        return token

from werkzeug.exceptions import Unauthorized
from flask import current_app


class UAuth(object):
    """API Authentication extension for Flask"""

    def __init__(self, app=None, authentication_callback=None):
        """Create a new UAuth object

        :param Flask app: the Flask object on wich to use
        :param func authentication_callback: the authentication callback
        function
        """
        self.app = app
        self.authentication_callback = authentication_callback

        if app is not None:
            self.init_app(
                app=app,
                authentication_callback=self.authentication_callback
            )

    @property
    def auth_header(self):
        """Get the header to use for authentication

        The default authentication header is 'Authorization'

        :rtype str
        :return: the authentication header
        """
        app = self._get_app()

        return app.config.get("UAUTH_AUTHENTICATION_HEADER", "Authorization")

    @property
    def auth_argument(self):
        """Get the argument to use for authentication

        :rtype: str
        :return: the authentication argument
        """
        app = self._get_app()

        return app.config.get("UAUTH_AUTHENTICATION_ARGUMENT")

    def _get_app(self):
        return self.app or current_app

    def _handle_unauthorized_user(self):
        raise Unauthorized()

    def _handle_missing_token(self):
        raise Unauthorized()

    def init_app(self, app, authentication_callback=None):
        """Initialize the authentication extention

        :param Flask app: the Flask object on wich to use
        :param func authentication_callback: the authentication callback
        function
        """
        self.authentication_callback = (
                authentication_callback or self.authentication_callback)

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["uauth"] = self

    def get_token(self, authorization_value):
        """Retrieve the token object

        The callback function should return None if the token doesn't exist

        :param str authorization_value: the value to use in order to search
        and retrieve the token object
        :rtype: TokenMixin|None
        :return: the Token object
        """
        return self.authentication_callback(authorization_value)

    def authenticate_request(self, request):
        """Authenticate the Flask request

        :param Request request: the Flask request object
        :rtype: TokenMixin|None
        :return: the token object
        """
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

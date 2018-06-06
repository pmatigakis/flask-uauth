from werkzeug.exceptions import Unauthorized


class UAuth(object):
    def __init__(self, app=None, authentication_callback=None, header=None,
                 argument=None):
        self.app = app
        self.authentication_callback = authentication_callback
        self.header = header or "Authorization"
        self.argument = argument

        if app is not None:
            self.init_app(
                app=app,
                authentication_callback=self.authentication_callback,
                header=self.header,
                argument=self.argument
            )

    def _handle_unauthorized_user(self):
        raise Unauthorized()

    def _handle_missing_token(self):
        raise Unauthorized()

    def init_app(self, app, authentication_callback=None, header=None,
                 argument=None):
        self.authentication_callback = (
                authentication_callback or self.authentication_callback)
        self.header = header or self.header
        self.argument = argument or self.argument

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["uauth"] = self

    def get_token(self, authorization_value):
        return self.authentication_callback(authorization_value)

    def authenticate_request(self, request):
        authorization_value = None

        if self.header is not None:
            authorization_value = request.headers.get(self.header)

        if authorization_value is None and self.argument is not None:
            authorization_value = request.args.get(self.argument)

        if authorization_value is None:
            return self._handle_missing_token()

        token = self.get_token(authorization_value)
        if token is None or not token.is_active():
            return self._handle_unauthorized_user()

        return token

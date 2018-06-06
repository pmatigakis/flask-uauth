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

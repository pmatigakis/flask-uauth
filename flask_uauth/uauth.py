class UAuth(object):
    def __init__(self, app=None, authentication_callback=None):
        self.app = app
        self.authentication_callback = authentication_callback

        if app is not None:
            self.init_app(app, self.authentication_callback)

    def init_app(self, app, authentication_callback=None):
        self.authentication_callback = (
                authentication_callback or self.authentication_callback)

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["uauth"] = self

    def get_token(self, authorization_value):
        return self.authentication_callback(authorization_value)

from flask import Flask

from flask_uauth import (
    UAuth, authentication_required, current_token, TokenMixin
)


uauth = UAuth()


class Token(TokenMixin):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<Token value={} active={}>".format(self.value, self.is_active())

    def __str__(self):
        return self.value


def authentication_callback(authorization_value):
    if authorization_value == "abc":
        return Token("abc")
    else:
        return None


@authentication_required
def index():
    return "accessed protected view using token '{}'".format(current_token.value)


def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", "index", index)
    uauth.init_app(app, authentication_callback)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

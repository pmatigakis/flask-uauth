from functools import wraps

from flask import request, current_app
from flask import _request_ctx_stack


def authentication_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        uauth = current_app.extensions["uauth"]
        authorization_value = None

        if uauth.header is not None:
            authorization_value = request.headers.get(uauth.header)

        if authorization_value is None and uauth.argument is not None:
            authorization_value = request.args.get(uauth.argument)

        if authorization_value is None:
            return uauth._handle_missing_token()

        token = uauth.get_token(authorization_value)
        if token is None or not token.is_active():
            return uauth._handle_unauthorized_user()

        _request_ctx_stack.top.current_token = token

        return f(*args, **kwargs)
    return wrapper

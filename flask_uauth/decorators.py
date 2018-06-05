from functools import wraps

from flask import request, current_app
from flask import _request_ctx_stack
from werkzeug.exceptions import Unauthorized


def authentication_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        authorization_value = request.headers.get("Authorization")
        if authorization_value is None:
            raise Unauthorized()

        uauth = current_app.extensions["uauth"]
        token = uauth.get_token(authorization_value)
        if token is None or not token.is_active():
            raise Unauthorized()

        _request_ctx_stack.top.current_token = token

        return f(*args, **kwargs)
    return wrapper

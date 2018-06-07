from unittest import TestCase, main

from flask import Flask

from flask_uauth import UAuth, authentication_required, TokenMixin


class Token(TokenMixin):
    def __init__(self, value, active):
        self.value = value
        self.active = active


class UAuthTests(TestCase):
    def setUp(self):
        self.app = Flask(__name__)

        def authentication_callback(authorization_value):
            if authorization_value == "active_token":
                return Token(authorization_value, True)
            elif authorization_value == "disabled_token":
                return Token(authorization_value, False)

            return None

        @self.app.route("/protected")
        @authentication_required
        def protected():
            return("this view is protected")

        @self.app.route("/public")
        def public():
            return ("this view is not protected")

        self.uauth = UAuth(self.app, authentication_callback)

    def test_do_not_allow_access_to_protected_view_without_token(self):
        response = self.app.test_client().get("/protected")

        self.assertEqual(response.status_code, 401)
        self.assertIn(b"The server could not verify that you are authorized "
                      b"to access the URL requested", response.data)

    def test_do_not_allow_access_to_protected_view_with_disabled_token(self):
        response = self.app.test_client().get(
            "/protected",
            headers={"Authorization": "disabled_token"}
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn(b"The server could not verify that you are authorized "
                      b"to access the URL requested", response.data)

    def test_do_not_allow_access_to_protected_view_with_unknown_token(self):
        response = self.app.test_client().get(
            "/protected",
            headers={"Authorization": "unknown_token"}
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn(b"The server could not verify that you are authorized "
                      b"to access the URL requested", response.data)

    def test_allow_access_to_protected_view_with_token(self):
        response = self.app.test_client().get(
            "/protected",
            headers={"Authorization": "active_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"this view is protected", response.data)

    def test_allow_access_to_unprotected_view_with_token(self):
        response = self.app.test_client().get(
            "/public",
            headers={"Authorization": "active_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"this view is not protected", response.data)

    def test_allow_access_to_unprotected_view_without_token(self):
        response = self.app.test_client().get("/public")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"this view is not protected", response.data)

    def test_token_is_not_cached_between_requests(self):
        response = self.app.test_client().get(
            "/protected",
            headers={"Authorization": "active_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"this view is protected", response.data)

        for token in ["unknown_token", "disabled_token"]:
            response = self.app.test_client().get(
                "/protected",
                headers={"Authorization": token}
            )

            self.assertEqual(response.status_code, 401)
            self.assertIn(
                b"The server could not verify that you are authorized "
                b"to access the URL requested", response.data)

        response = self.app.test_client().get("/protected")

        self.assertEqual(response.status_code, 401)
        self.assertIn(b"The server could not verify that you are authorized "
                      b"to access the URL requested", response.data)


if __name__ == "__main__":
    main()

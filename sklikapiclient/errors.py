# -*- coding: utf-8 -*-


class AuthError(Exception):
    pass


class LoginAuthError(AuthError):
    pass


class TokenAuthError(AuthError):
    pass


class SessionExpiredError(AuthError):
    pass

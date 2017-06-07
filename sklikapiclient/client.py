# -*- coding: utf-8 -*-


import requests
from . import config, errors


class Sklik(object):

    def __init__(self, username=None, password=None, api_key=None,
                 api_url=config.SKLIK_URL, user_agent=config.USER_AGENT):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.api_url = api_url
        self.user_agent = user_agent

    def _login_method(self):
        """Login via username and password.

        :return: HTTP response
        """
        method = 'client.login'
        credentials = [self.username, self.password]
        session = self._post(method, *credentials).get('session')
        if session is None:
            raise errors.LoginAuthError("Session not found.")
        return session

    def _token_method(self):
        """Login via API key.

        :return: HTTP response
        """
        method = 'client.loginByToken'
        session = self._post(method, self.api_key).get('session')
        if session is None:
            raise errors.TokenAuthError("Session not found.")
        return session

    def login(self):
        """Return session, otherwise raise exception.

        :return: session
        """
        if self.api_key:
            return self._token_method()
        elif self.username and self.password:
            return self._login_method()
        else:
            raise errors.AuthError(
                'Either login and username or '
                'api key must be given to authenticate.')

    def _post(self, method, *parameters):
        """Encapsulation of the HTTP POST method as used in Sklik API.

        :param method: Sklik API method. Eg: campaigns.create
        :param args: optional data
        :return: result of POST method
        """
        response = requests.post(self.api_url + method, json=parameters)
        response.raise_for_status()
        return response.json()

    def post(self, method, *parameters):
        """Encapsulation HTTP POST method.

        :param method: Sklik API method. Eg: campaigns.create
        :param args: optional data
        :return: result of POST method
        """
        try:
            return self._post(method, *parameters)
        except requests.RequestException as e:
            response = getattr(e, 'response', None)
            if response is None or response.status_code != 401 or \
               'Session has expired' not in response.content:
                raise e
            raise errors.SessionExpiredError("Session is expired.")

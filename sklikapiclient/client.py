# -*- coding: utf-8 -*-

from config import SKLIK_URL
from requests import post, get


class Sklik(object):

    def __init__(self, username=None, password=None, api_key=None):
        self.url = SKLIK_URL
        self.username = username
        self.password = password
        self.api_key = api_key
        self.session = None

    def _login_method(self):
        """Login via username and password.
        :return: HTTP response
        """
        method = 'client.login'
        login_response = post(self.url + method,
                              json=(self.username, self.password))
        return self._parse_login(login_response)

    def _token_method(self):
        """Login via API key.
        :return: HTTP response
        """
        method = 'client.loginByToken'
        login_response = post(self.url + method, json=(self.api_key, ))
        return self._parse_login(login_response)

    def _parse_login(self, login_response):
        """Login via username and password or API key returns response.
        Session is saved or exception is raised.
        :param login_response: HTTP response
        """
        response = login_response.json()
        if response['status'] == 200:
            self.session = response['session']
        else:
            raise Exception('login fail')

    def _login(self):
        """Return session, otherwise raise exception.
        :return: session
        """
        if not self.session:
            if self.api_key:
                self._token_method()
            elif self.username and self.password:
                self._login_method()

        return self.session

    def get(self, method, **kwargs):
        """Encapsulation HTTP GET method.
        :param method: Sklik API method. Eg: client.getCredit
        :param kwargs: optional data
        :return: result of GET method
        """
        kwargs['session'] = self._login()
        return get(self.url + method, json=[kwargs]).json()

    def post(self, method, *args):
        """Encapsulation HTTP POST method.
        :param method: Sklik API method. Eg: campaigns.create
        :param args: optional data
        :return: result of POST method
        """
        json_list = [list(args)]
        json_list.insert(0, {'session': self._login()})
        return post(self.url + method, data=None, json=json_list).json()

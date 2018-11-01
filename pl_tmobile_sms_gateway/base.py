# -*- coding: utf-8 -*-

import abc
import re
import requests
from requests.compat import quote
from .exceptions import SmsException
from .models import GatewayResponse


class Base:
    DEFAULT_RETURN_URL = "http://www.t-mobile.pl"

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send(self, number, message):
        params = {
            "login": self.login,
            "password": self.password,
            "number": number,
            "message": message.encode("ISO-8859-2"),
            "mms": "false",
            "failure": self.DEFAULT_RETURN_URL,
            "success": self.DEFAULT_RETURN_URL
        }
        # requests uses internally urllib's quote_plus for url encoding, which results in spaces
        # being encoded to '+'
        url = self._build_url(params)
        response = requests.get(url, allow_redirects=False)
        if not response.ok:
            raise SmsException("Error while sending an sms [{}]".format(response.status_code))
        tokens_left = self._tokens_left(response)
        error_code = self._error_code(response)
        message = self._humanize_error(error_code)
        return GatewayResponse(ok=error_code == 0, message=message, tokens_left=tokens_left)

    @abc.abstractmethod
    def base_url(self):
        pass

    def _build_url(self, params):
        query_parts = ["{}={}".format(name, quote(value)) for name, value in params.items()]
        query = "&".join(query_parts)
        return "{}?{}".format(self.base_url(), query)

    def _error_code(self, response):
        code = self._parse_location_header(response, "error")
        if code is None:
            raise SmsException("Expecting error code in 'location' header, none was found")
        return code

    def _tokens_left(self, response):
        return self._parse_location_header(response, "tokens")

    @staticmethod
    def _parse_location_header(response, type):
        if "location" in response.headers:
            location = response.headers["location"]
            match = re.search("x-era-{}=(\d+)".format(type), location, flags=re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    @staticmethod
    def _humanize_error(code):
        errors = {
            0: "wysyłka bez błędu",
            1: "awaria systemu",
            2: "użytkownik nieautoryzowany",
            3: "dostęp zablokowany",
            5: "błąd składni",
            7: "wyczerpany limit",
            8: "błędny adres odbiorcy",
            9: "wiadomość zbyt długa",
            10: "brak wymaganej liczby żetonów"
        }
        if code not in errors:
            return "nieznany błąd"
        return errors[code]

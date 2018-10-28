# -*- coding: utf-8 -*-

import unittest
import requests_mock
from pl_tmobile_sms_gateway import (Omnix, SmsException)

RECEIVER_NUMBER = "01234567"
TEXT = "Some text"
URL = "http://www.t-mobile.pl/msg/api/do/tinker/omnix"


class BasicTestSuite(unittest.TestCase):

    def setUp(self):
        self.omnix = Omnix("login", "password", return_url="example.com")

    def test_success(self):
        with requests_mock.mock() as mock:
            mock.get(URL, status_code=302, headers={"location": "http://example.com?X-ERA-error=0&X-ERA-tokens=10"})
            r = self.omnix.send(RECEIVER_NUMBER, TEXT)
            assert r.ok
            assert r.tokens_left == 10

    def test_is_case_insensitive(self):
        with requests_mock.mock() as mock:
            mock.get(URL, status_code=302, headers={"location": "http://example.com?x-era-error=0&x-era-tokens=10"})
            r = self.omnix.send(RECEIVER_NUMBER, TEXT)
            assert r.ok
            assert r.tokens_left == 10

    def test_error_code(self):
        with requests_mock.mock() as m:
            m.get(URL, status_code=302, headers={"location": "http://example.com?X-ERA-error=1"})
            r = self.omnix.send(RECEIVER_NUMBER, TEXT)
            assert not r.ok

    def test_missing_error_code(self):
        with requests_mock.mock() as m:
            m.get(URL, status_code=302, headers={"location": "http://example.com"})
            with self.assertRaises(SmsException):
                self.omnix.send(RECEIVER_NUMBER, TEXT)

    def test_missing_location_header(self):
        with requests_mock.mock() as m:
            m.get(URL, status_code=302)
            with self.assertRaises(SmsException):
                self.omnix.send(RECEIVER_NUMBER, TEXT)

    def test_endpoint_not_found(self):
        with requests_mock.mock() as m:
            m.get(URL, status_code=404)
            with self.assertRaises(SmsException):
                self.omnix.send(RECEIVER_NUMBER, TEXT)


if __name__ == '__main__':
    unittest.main()

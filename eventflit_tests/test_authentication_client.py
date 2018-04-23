# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

import os
import six
import hmac
import json
import hashlib
import unittest
import time
from decimal import Decimal

from eventflit.authentication_client import AuthenticationClient
from eventflit.signature import sign, verify

try:
    import unittest.mock as mock
except ImportError:
    import mock


class TestAuthenticationClient(unittest.TestCase):
    def test_authenticate_for_private_channels(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        expected = {
            u'auth': u"foo:89955e77e1b40e33df6d515a5ecbba86a01dc816a5b720da18a06fd26f7d92ff"
        }

        self.assertEqual(authenticationClient.authenticate(u'private-channel', u'345.23'), expected)


    def test_authenticate_types(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        self.assertRaises(TypeError, lambda: authenticationClient.authenticate(2423, u'34554'))
        self.assertRaises(TypeError, lambda: authenticationClient.authenticate(u'plah', 234234))
        self.assertRaises(ValueError, lambda: authenticationClient.authenticate(u'::', u'345345'))


    def test_authenticate_for_presence_channels(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        custom_data = {
            u'user_id': u'fred',
            u'user_info': {
                u'key': u'value'
            }
        }

        expected = {
            u'auth': u"foo:e80ba6439492c2113022c39297a87a948de14061cc67b5788e045645a68b8ccd",
            u'channel_data': u"{\"user_id\":\"fred\",\"user_info\":{\"key\":\"value\"}}"
        }

        with mock.patch('json.dumps', return_value=expected[u'channel_data']) as dumps_mock:
            actual = authenticationClient.authenticate(u'presence-channel', u'345.43245', custom_data)

        self.assertEqual(actual, expected)
        dumps_mock.assert_called_once_with(custom_data, cls=None)


    def test_validate_webhook_success_case(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        body = u'{"time_ms": 1000000}'
        signature = six.text_type(hmac.new(authenticationClient.secret.encode('utf8'), body.encode('utf8'), hashlib.sha256).hexdigest())

        with mock.patch('time.time', return_value=1200):
            self.assertEqual(authenticationClient.validate_webhook(authenticationClient.key, signature, body), {u'time_ms': 1000000})


    def test_validate_webhook_bad_types(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        authenticationClient.validate_webhook(u'key', u'signature', u'body')

        # These things are meant to be human readable, so enforcing being
        # text is sensible.

        with mock.patch('time.time') as time_mock:
            self.assertRaises(TypeError, lambda: authenticationClient.validate_webhook(4, u'signature', u'body'))
            self.assertRaises(TypeError, lambda: authenticationClient.validate_webhook(u'key', 4, u'body'))
            self.assertRaises(TypeError, lambda: authenticationClient.validate_webhook(u'key', u'signature', 4))

        time_mock.assert_not_called()


    def test_validate_webhook_bad_key(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        body = u'some body'
        signature = six.text_type(hmac.new(authenticationClient.secret.encode(u'utf8'), body.encode(u'utf8'), hashlib.sha256).hexdigest())

        with mock.patch('time.time') as time_mock:
            self.assertEqual(authenticationClient.validate_webhook(u'badkey', signature, body), None)

        time_mock.assert_not_called()


    def test_validate_webhook_bad_signature(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        body = u'some body'
        signature = u'some signature'

        with mock.patch('time.time') as time_mock:
            self.assertEqual(
                authenticationClient.validate_webhook(
                    authenticationClient.key, signature, body), None)

        time_mock.assert_not_called()


    def test_validate_webhook_bad_time(self):
        authenticationClient = AuthenticationClient(
            key=u'foo', secret=u'bar', host=u'host', app_id=u'4', ssl=True)

        body = u'{"time_ms": 1000000}'
        signature = six.text_type(
            hmac.new(
                authenticationClient.secret.encode('utf8'),
                body.encode('utf8'), hashlib.sha256).hexdigest())

        with mock.patch('time.time', return_value=1301):
            self.assertEqual(authenticationClient.validate_webhook(
                authenticationClient.key, signature, body), None)


class TestJson(unittest.TestCase):
    def setUp(self):
        class JSONEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, Decimal):
                    return str(o)

                return super(JSONEncoder, self).default(o)

        constants = {"NaN": 99999}

        class JSONDecoder(json.JSONDecoder):
            def __init__(self, **kwargs):
                super(JSONDecoder, self).__init__(
                    parse_constant=constants.__getitem__)

        self.authentication_client = AuthenticationClient(
            "4", "key", "secret", host="somehost", json_encoder=JSONEncoder,
            json_decoder=JSONDecoder)


    def test_custom_json_decoder(self):
        t = 1000 * time.time()
        body = u'{"nan": NaN, "time_ms": %f}' % t
        signature = sign(self.authentication_client.secret, body)
        data = self.authentication_client.validate_webhook(
            self.authentication_client.key, signature, body)
        self.assertEqual({u"nan": 99999, u"time_ms": t}, data)


    def test_custom_json_encoder(self):
        expected = {
            u'channel_data': '{"money": "1.32"}',
            u'auth': u'key:7f2ae5922800a20b9615543ce7c8e7d1c97115d108939410825ea690f308a05f'
        }
        data = self.authentication_client.authenticate("presence-c1", "1.1", {"money": Decimal("1.32")})
        self.assertEqual(expected, data)


if __name__ == '__main__':
    unittest.main()

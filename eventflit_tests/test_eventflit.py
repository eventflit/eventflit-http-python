# -*- coding: utf-8 -*-

from __future__ import (
    print_function,
    unicode_literals,
    absolute_import,
    division)

import hashlib
import hmac
import os
import six
import unittest

from eventflit.eventflit import Eventflit

try:
    import unittest.mock as mock
except ImportError:
    import mock


class TestEventflit(unittest.TestCase):
    def test_initialize_from_url(self):
        self.assertRaises(TypeError, lambda: Eventflit.from_url(4))
        self.assertRaises(Exception, lambda: Eventflit.from_url(u'httpsahsutaeh'))

        eventflit = Eventflit.from_url(u'http://foo:bar@host/apps/4')
        self.assertEqual(eventflit._eventflit_client.ssl, False)
        self.assertEqual(eventflit._eventflit_client.key, u'foo')
        self.assertEqual(eventflit._eventflit_client.secret, u'bar')
        self.assertEqual(eventflit._eventflit_client.host, u'host')
        self.assertEqual(eventflit._eventflit_client.app_id, u'4')

        eventflit = Eventflit.from_url(u'https://foo:bar@host/apps/4')
        self.assertEqual(eventflit._eventflit_client.ssl, True)
        self.assertEqual(eventflit._eventflit_client.key, u'foo')
        self.assertEqual(eventflit._eventflit_client.secret, u'bar')
        self.assertEqual(eventflit._eventflit_client.host, u'host')
        self.assertEqual(eventflit._eventflit_client.app_id, u'4')

    def test_initialize_from_env(self):
        with mock.patch.object(os, 'environ', new={'EVENTFLIT_URL':'https://plah:bob@somehost/apps/42'}):
            eventflit = Eventflit.from_env()
            self.assertEqual(eventflit._eventflit_client.ssl, True)
            self.assertEqual(eventflit._eventflit_client.key, u'plah')
            self.assertEqual(eventflit._eventflit_client.secret, u'bob')
            self.assertEqual(eventflit._eventflit_client.host, u'somehost')
            self.assertEqual(eventflit._eventflit_client.app_id, u'42')


if __name__ == '__main__':
    unittest.main()

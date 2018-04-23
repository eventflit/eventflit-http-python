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

from eventflit.eventflit_client import EventflitClient
from eventflit.http import GET

try:
    import unittest.mock as mock
except ImportError:
    import mock

class TestEventflitClient(unittest.TestCase):
    def setUp(self):
        self.eventflit_client = EventflitClient(app_id=u'4', key=u'key', secret=u'secret', host=u'somehost')

    def test_host_should_be_text(self):
        EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True, host=u'foo')

        self.assertRaises(TypeError, lambda: EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True, host=4))

    def test_cluster_should_be_text(self):
        EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True, cluster=u'eu')

        self.assertRaises(TypeError, lambda: EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True, cluster=4))

    def test_host_behaviour(self):
        conf = EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True)
        self.assertEqual(conf.host, u'service.eventflit.com', u'default host should be correct')

        conf = EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True, cluster=u'eu')
        self.assertEqual(conf.host, u'api-eu.eventflit.com', u'host should be overriden by cluster setting')

        conf = EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True, host=u'foo')
        self.assertEqual(conf.host, u'foo', u'host should be overriden by host setting')

        conf = EventflitClient(app_id=u'4', key=u'key', secret=u'secret', ssl=True, cluster=u'eu', host=u'plah')
        self.assertEqual(conf.host, u'plah', u'host should be used in preference to cluster')

    def test_trigger_with_channels_list_success_case(self):
        json_dumped = u'{"message": "hello world"}'

        with mock.patch('json.dumps', return_value=json_dumped) as json_dumps_mock:
            request = self.eventflit_client.trigger.make_request([u'some_channel'], u'some_event', {u'message': u'hello world'})

            self.assertEqual(request.path, u'/apps/4/events')
            self.assertEqual(request.method, u'POST')

            expected_params = {
                u'channels': [u'some_channel'],
                u'data': json_dumped,
                u'name': u'some_event'
            }

            self.assertEqual(request.params, expected_params)

        # FIXME: broken
        #json_dumps_mock.assert_called_once_with({u'message': u'hello world'})

    def test_trigger_with_channel_string_success_case(self):
        json_dumped = u'{"message": "hello worlds"}'

        with mock.patch('json.dumps', return_value=json_dumped) as json_dumps_mock:

            request = self.eventflit_client.trigger.make_request(u'some_channel', u'some_event', {u'message': u'hello worlds'})

            expected_params = {
                u'channels': [u'some_channel'],
                u'data': json_dumped,
                u'name': u'some_event'
            }

            self.assertEqual(request.params, expected_params)

    def test_trigger_batch_success_case(self):
        json_dumped = u'{"message": "something"}'

        with mock.patch('json.dumps', return_value=json_dumped) as json_dumps_mock:

            request = self.eventflit_client.trigger_batch.make_request([{
                        u'channel': u'my-chan',
                        u'name': u'my-event',
                        u'data': {u'message': u'something'}
                    }])

            expected_params = {
                u'batch': [{
                    u'channel': u'my-chan',
                    u'name': u'my-event',
                    u'data': json_dumped
                }]
            }

            self.assertEqual(request.params, expected_params)


    def test_trigger_disallow_non_string_or_list_channels(self):
        self.assertRaises(TypeError, lambda:
            self.eventflit_client.trigger.make_request({u'channels': u'test_channel'}, u'some_event', {u'message': u'hello world'}))

    def test_trigger_disallow_invalid_channels(self):
        self.assertRaises(ValueError, lambda:
            self.eventflit_client.trigger.make_request([u'so/me_channel!'], u'some_event', {u'message': u'hello world'}))

    def test_channels_info_default_success_case(self):
        request = self.eventflit_client.channels_info.make_request()

        self.assertEqual(request.method, GET)
        self.assertEqual(request.path, u'/apps/4/channels')
        self.assertEqual(request.params, {})

    def test_channels_info_with_prefix_success_case(self):
        request = self.eventflit_client.channels_info.make_request(prefix_filter='test')

        self.assertEqual(request.method, GET)
        self.assertEqual(request.path, u'/apps/4/channels')
        self.assertEqual(request.params, {u'filter_by_prefix': u'test'})

    def test_channels_info_with_attrs_success_case(self):
        request = self.eventflit_client.channels_info.make_request(attributes=[u'attr1', u'attr2'])

        self.assertEqual(request.method, GET)
        self.assertEqual(request.path, u'/apps/4/channels')
        self.assertEqual(request.params, {u'info': u'attr1,attr2'})

    def test_channel_info_success_case(self):
        request = self.eventflit_client.channel_info.make_request(u'some_channel')

        self.assertEqual(request.method, GET)
        self.assertEqual(request.path, u'/apps/4/channels/some_channel')
        self.assertEqual(request.params, {})

    def test_channel_info_with_attrs_success_case(self):
        request = self.eventflit_client.channel_info.make_request(u'some_channel', attributes=[u'attr1', u'attr2'])

        self.assertEqual(request.method, GET)
        self.assertEqual(request.path, u'/apps/4/channels/some_channel')
        self.assertEqual(request.params, {u'info': u'attr1,attr2'})

    def test_user_info_success_case(self):
        request = self.eventflit_client.users_info.make_request(u'presence-channel')

        self.assertEqual(request.method, GET)
        self.assertEqual(request.path, u'/apps/4/channels/presence-channel/users')
        self.assertEqual(request.params, {})


if __name__ == '__main__':
    unittest.main()

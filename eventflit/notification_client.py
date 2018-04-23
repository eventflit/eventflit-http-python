# -*- coding: utf-8 -*-

from __future__ import (
    print_function,
    unicode_literals,
    absolute_import,
    division)

from eventflit.client import Client
from eventflit.http import POST, Request, request_method
from eventflit.util import ensure_text


DEFAULT_HOST = "push.eventflit.com"
RESTRICTED_GCM_KEYS = ['to', 'registration_ids']
API_PREFIX = 'publisher/app/'
GCM_TTL = 241920

class NotificationClient(Client):
    def __init__(
            self, app_id, key, secret, ssl=True, host=None, port=None,
            timeout=30, cluster=None, json_encoder=None, json_decoder=None,
            backend=None, **backend_options):
        super(NotificationClient, self).__init__(
            app_id, key, secret, ssl, host, port, timeout, cluster,
            json_encoder, json_decoder, backend, **backend_options)

        if host:
            self._host = ensure_text(host, "host")

        else:
            self._host = DEFAULT_HOST


    @request_method
    def notify(self, interests, notification):
        """Send push notifications, see:

        https://github.com/eventflit/eventflit-http-python#push-notifications-beta
        """
        if not isinstance(interests, list) and not isinstance(interests, set):
            raise TypeError("Interests must be a list or a set")

        if len(interests) is 0:
            raise ValueError("Interests must not be empty")

        if not isinstance(notification, dict):
            raise TypeError("Notification must be a dictionary")

        params = {
            'interests': interests}

        params.update(notification)
        path = (
            "%s/%s/publishes" %
            (API_PREFIX, self.app_id))

        return Request(self, POST, path, params)

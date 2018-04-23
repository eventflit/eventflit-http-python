# -*- coding: utf-8 -*-

from __future__ import (
    print_function,
    unicode_literals,
    absolute_import,
    division)

import collections
import hashlib
import os
import re
import six
import time

from eventflit.util import (
    ensure_text,
    eventflit_url_re,
    doc_string)

from eventflit.eventflit_client import EventflitClient
from eventflit.notification_client import NotificationClient
from eventflit.authentication_client import AuthenticationClient


class Eventflit(object):
    """Client for the Eventflit HTTP API.

    This client supports various backend adapters to support various http
    libraries available in the python ecosystem.

    :param app_id:  a eventflit application identifier
    :param key:     a eventflit application key
    :param secret:  a eventflit application secret token
    :param ssl:     Whenever to use SSL or plain HTTP
    :param host:    Used for custom host destination
    :param port:    Used for custom port destination
    :param timeout: Request timeout (in seconds)
    :param cluster: Convention for other clusters than the main Eventflit-one.
      Eg: 'eu' will resolve to the api-eu.eventflitapp.com host
    :param backend: an http adapter class (AsyncIOBackend, RequestsBackend,
      SynchronousBackend, TornadoBackend)
    :param backend_options: additional backend
    """
    def __init__(
            self, app_id, key, secret, ssl=True, host=None, port=None,
            timeout=5, cluster=None, json_encoder=None, json_decoder=None,
            backend=None, notification_host=None, notification_ssl=True,
            **backend_options):
        self._eventflit_client = EventflitClient(
            app_id, key, secret, ssl, host, port, timeout, cluster,
            json_encoder, json_decoder, backend, **backend_options)

        self._authentication_client = AuthenticationClient(
            app_id, key, secret, ssl, host, port, timeout, cluster,
            json_encoder, json_decoder, backend, **backend_options)

        self._notification_client = NotificationClient(
            app_id, key, secret, notification_ssl, notification_host, port,
            timeout, cluster, json_encoder, json_decoder, backend,
            **backend_options)


    @classmethod
    def from_url(cls, url, **options):
        """Alternative constructor that extracts the information from a URL.

        :param url: String containing a URL

        Usage::

          >> from eventflit import Eventflit
          >> p =
            Eventflit.from_url("http://mykey:mysecret@eventflit.com/apps/432")
        """
        m = eventflit_url_re.match(ensure_text(url, "url"))
        if not m:
            raise Exception("Unparsable url: %s" % url)

        ssl = m.group(1) == 'https'

        options_ = {
            'key': m.group(2),
            'secret': m.group(3),
            'host': m.group(4),
            'app_id': m.group(5),
            'ssl': ssl}

        options_.update(options)

        return cls(**options_)


    @classmethod
    def from_env(cls, env='EVENTFLIT_URL', **options):
        """Alternative constructor that extracts the information from an URL
        stored in an environment variable. The eventflit heroku addon will set
        the EVENTFLIT_URL automatically when installed for example.

        :param env: Name of the environment variable

        Usage::

          >> from eventflit import Eventflit
          >> c = Eventflit.from_env("EVENTFLIT_URL")
        """
        val = os.environ.get(env)
        if not val:
            raise Exception("Environment variable %s not found" % env)

        return cls.from_url(val, **options)


    @doc_string(EventflitClient.trigger.__doc__)
    def trigger(self, channels, event_name, data, socket_id=None):
        return self._eventflit_client.trigger(
            channels, event_name, data, socket_id)


    @doc_string(EventflitClient.trigger_batch.__doc__)
    def trigger_batch(self, batch=[], already_encoded=False):
        return self._eventflit_client.trigger_batch(batch, already_encoded)


    @doc_string(EventflitClient.channels_info.__doc__)
    def channels_info(self, prefix_filter=None, attributes=[]):
        return self._eventflit_client.channels_info(prefix_filter, attributes)


    @doc_string(EventflitClient.channel_info.__doc__)
    def channel_info(self, channel, attributes=[]):
        return self._eventflit_client.channel_info(channel, attributes)


    @doc_string(EventflitClient.users_info.__doc__)
    def users_info(self, channel):
        return self._eventflit_client.users_info(channel)


    @doc_string(AuthenticationClient.authenticate.__doc__)
    def authenticate(self, channel, socket_id, custom_data=None):
        return self._authentication_client.authenticate(
            channel, socket_id, custom_data)


    @doc_string(AuthenticationClient.validate_webhook.__doc__)
    def validate_webhook(self, key, signature, body):
        return self._authentication_client.validate_webhook(
            key, signature, body)


    @doc_string(NotificationClient.notify.__doc__)
    def notify(self, interest, notification):
        return self._notification_client.notify(interest, notification)

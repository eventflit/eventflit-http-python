# -*- coding: utf-8 -*-

from __future__ import (
    print_function,
    unicode_literals,
    absolute_import,
    division)


class EventflitError(Exception):
    pass


class EventflitBadRequest(EventflitError):
    pass


class EventflitBadAuth(EventflitError):
    pass


class EventflitForbidden(EventflitError):
    pass


class EventflitBadStatus(EventflitError):
    pass

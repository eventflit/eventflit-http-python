# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

from eventflit import Eventflit
import unittest
import httpretty

class TestRequestsBackend(unittest.TestCase):

  def setUp(self):
    self.eventflit = Eventflit.from_url(u'http://key:secret@service.eventflit.com/apps/4')

  @httpretty.activate
  def test_trigger_requests_success(self):
    httpretty.register_uri(httpretty.POST, "http://service.eventflit.com/apps/4/events",
                       body="{}",
                       content_type="application/json")
    response = self.eventflit.trigger(u'test_channel', u'test', {u'data': u'yolo'})
    self.assertEqual(response, {})


if __name__ == '__main__':
    unittest.main()

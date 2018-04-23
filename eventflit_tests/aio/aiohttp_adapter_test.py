from __future__ import print_function, absolute_import, division

import eventflit
import eventflit.aiohttp
import asyncio
import unittest
import httpretty

class TestAIOHTTPBackend(unittest.TestCase):

  def setUp(self):
    self.p = eventflit.Eventflit.from_url(u'http://key:secret@service.eventflit.com/apps/4',
                                  backend=eventflit.aiohttp.AsyncIOBackend)

  @httpretty.activate
  def test_trigger_aio_success(self):
    httpretty.register_uri(httpretty.POST, "http://service.eventflit.com/apps/4/events",
                       body="{}",
                       content_type="application/json")
    response = yield from self.p.trigger(u'test_channel', u'test', {u'data': u'yolo'})
    self.assertEqual(response, {})

if __name__ == '__main__':
    unittest.main()

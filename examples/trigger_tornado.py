import eventflit
import eventflit.tornado
import tornado.ioloop

ioloop = tornado.ioloop.IOLoop.instance()

def show_response(response):
    print(response.result())
    ioloop.stop()

client = eventflit.Eventflit.from_env(
            backend=eventflit.tornado.TornadoBackend,
            timeout=50
         )
response = client.trigger("hello", "world", dict(foo='bar'))
response.add_done_callback(show_response)
print("Before start")
ioloop.start()
print("After start")

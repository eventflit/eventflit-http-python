import eventflit
import eventflit.aiohttp
import asyncio

def main():
    client = eventflit.Eventflit.from_env(
            backend=eventflit.aiohttp.AsyncIOBackend,
            timeout=50
            )
    print("before trigger")
    response = yield from client.trigger("hello", "world", dict(foo='bar'))
    print(response)

asyncio.get_event_loop().run_until_complete(main())

from . import BaseServer, FormField, QueryField


class TestServer(BaseServer):
    URL = 'http://www.baidu.com'
    TIMEOUT = 5
    HEADERS = {}
    name = FormField(required=True, default='alex')
    age = QueryField(required=True)
    score = QueryField()


def sync_example():
    ts = TestServer(age=12, score=100).new_server()
    rsp = ts.fetch()
    print(rsp.content)


async def async_example():
    ts = TestServer(age=12, score=100).new_server()
    rsp = await ts.async_fetch()
    print(rsp.content)

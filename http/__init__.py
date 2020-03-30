import json
import logging
import traceback
from itertools import chain

import aiohttp
import requests


logger = logging.getLogger('__main__')


class Field(object):
    def __init__(self, default, required):
        self.default = default
        self.required = required

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.default)


class FormField(Field):
    def __init__(self, default=None, required=False):
        super(FormField, self).__init__(default, required)


class QueryField(Field):
    def __init__(self, default=None, required=False):
        super(QueryField, self).__init__(default, required)


class RequestMetaClass(type):
    def __new__(cls, name, bases, attrs):
        form_mapper = {}
        query_mapper = {}
        for k, v in attrs.items():
            if isinstance(v, FormField):
                form_mapper[k] = v
            if isinstance(v, QueryField):
                query_mapper[k] = v

        for k in chain(form_mapper.keys(), query_mapper.keys()):
            attrs.pop(k)

        attrs['__form_mapper__'] = form_mapper
        attrs['__query_mapper__'] = query_mapper

        return type.__new__(cls, name, bases, attrs)


class BaseServer(dict, object, metaclass=RequestMetaClass):
    # __metaclass__ = RequestMetaClass

    def __init__(self, **kwargs):
        super(BaseServer, self).__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('"BaseServer" has no attribute "%s"' % key)

    def set_headers(self, header):
        self.header = header

    def new_server(self):
        # self.set_headers()
        # self.method = self.METHOD
        # if self.__HOST__ == 'service_api':
        #     self.__mapper__['sign'] = jiami(self.__mapper__)
        # self.url = self.URL
        # self.timeout = self.TIMEOUT

        self.data = {}
        for mapper in chain(getattr(self, '__form_mapper__', {}), getattr(self, '__query_mapper__', {})):
            for k, v in mapper.items():
                vv = getattr(self, k, None) or v.default
                if v.required and vv == None:
                    raise AttributeError('<%s is required, found the given value is %s>' % (k, vv))
                self.data[k] = vv
        self.form, self.query = {}, {}
        for k, v in getattr(self, '__form_mapper__', {}).items():
            vv = getattr(self, k, None) or v.default
            if v.required and vv is None:
                raise AttributeError('<%s is required, found the given value is %s>' % (k, vv))
            self.data[k] = vv
        for k, v in getattr(self, '__query_mapper__', {}).items():
            vv = getattr(self, k, None) or v.default
            if v.required and vv is None:
                raise AttributeError('<%s is required, found the given value is %s>' % (k, vv))
            self.query[k] = vv

        return self

    def unserialize(self):
        try:
            return json.loads(self.response.content)
        except:
            logger.error('unserialize_err',
                         extra={'err': traceback.format_exc(), 'url': self.url, 'rsp': self.response.content,
                                'params': self.data})
            return {}

    def fetch(self):
        response = requests.request(self.METHOD,
                                    self.URL,
                                    params=self.query,
                                    data=self.form,
                                    headers=self.header,
                                    timeout=self.TIMEOUT)
        self.response = response
        return self.unserialize()

    async def async_fetch(self):
        async with aiohttp.ClientSession() as session:
            handle = getattr(session, self.METHOD.lower())
            timeout = aiohttp.ClientTimeout(total=self.TIMEOUT)
            async with handle(timeout=timeout, headers=self.header) as response:
                self.response = await response.text()
            return self.unserialize()

"""
class TestServer(BaseServer):
    URL = 'http://www.baidu.com'
    TIMEOUT = 5
    HEADERS = {}
    name = FormField(required=True, default='peter')
    age = FormField(required=True)
    sex = QueryField()

test = TestServer(age=12, sex='women')
ts = test.new_server()
rsp = ts.fetch()
"""
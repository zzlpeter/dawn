import sys
import os

import toml

from libs import singleton


@singleton
class Config:
    def __init__(self, file_path='conf/conf.toml', body=None):
        """
        解析toml配置文件
        """
        if body is not None:
            self.__conf = toml.loads(body)
        else:
            paths = sys.path
            for p in paths:
                abs_path = os.path.join(p, file_path)
                if os.path.isfile(abs_path):
                    with open(abs_path, encoding='utf-8') as cf:
                        self.__conf = toml.loads(cf.read())
                    break
            else:
                raise IOError

    @property
    def mysql(self):
        return self.__conf.get('database', {}).get('mysql', {})

    @property
    def redis(self):
        return self.__conf.get('database', {}).get('redis', {})

    @property
    def basic(self):
        return self.__conf.get('basic', None)

    @property
    def logger(self):
        return self.__conf.get('logger', {})

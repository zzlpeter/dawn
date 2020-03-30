import os
import socket
import uuid
import hashlib
import time
import random
import binascii
from functools import wraps

from pyDes import des, CBC, PAD_PKCS5


__all__ = [
    'singleton',
    'func_cache',
    'Host',
    'Environ',
    'DesSecret',
    'gen_uuid',
    'md5',
    'gen_auto_increment_id'
]


def singleton(cls):
    instance = dict()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper


def func_cache(func):
    cache_dict = dict()

    @wraps(func)
    def wrapper(*args, **kwargs):
        if func not in cache_dict:
            try:
                cache_dict[func] = func(*args, **kwargs)
            except Exception as e:
                raise e
        return cache_dict[func]
    return wrapper


class Host:
    """
    >>> host = Host()
    >>> host.host_ip
    >>> 172.25.4.68
    """
    @property
    @func_cache
    def host_ip(self):
        """
        查询本机ip地址
        """
        ip = None
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
            return ip

    @property
    @func_cache
    def host_name(self):
        """
        查询本机hostname
        """
        name = None
        try:
            if socket.gethostname().find('.') >= 0:
                name = socket.gethostname()
            else:
                name = socket.gethostbyaddr(socket.gethostname())[0]
        finally:
            return name


class Environ:
    """
    >>> env = Environ()
    >>> env.PYTHON_ENV = 'PRO'
    """
    def __setattr__(self, env, value):
        os.environ[env] = value

    def __getattr__(self, env):
        return os.environ.get(env, None)


class DesSecret:
    def __init__(self, secret_key=None):
        if secret_key is not None:
            if len(secret_key) != 8:
                raise Exception('秘钥:{}长度不等于8'.format(secret_key))
            self.key = secret_key
        else:
            self.key = 'mHAxsLYz'

    def des_encrypt(self, s):
        """
        DES 加密
        :param s: 原始字符串
        :return: 加密后字符串，16进制
        """
        secret_key = self.key
        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(s, padmode=PAD_PKCS5)
        return str(binascii.b2a_hex(en))

    def des_descrypt(self, s):
        """
        DES 解密
        :param s: 加密后的字符串，16进制
        :return:  解密后的字符串
        """
        secret_key = self.key
        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
        return de


def gen_uuid():
    """
    生成UUID
    """
    _uuid = str(uuid.uuid1())
    return _uuid.replace('-', '')


def md5(string):
    """
    md5加密
    """
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def gen_auto_increment_id():
    stamp = str(time.time() * 100000)
    rt = str(random.randint(0, 10000))
    rt.zfill(5)
    return f'{stamp}{rt}'

if __name__ == '__main__':
    print(Host.host_ip)
    print(Host().host_ip)

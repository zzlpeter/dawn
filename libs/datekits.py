import time
from datetime import datetime


__all__ = [
    'timestamp',
    'datetime_fmt'
]


def timestamp(mill=False):
    now = time.time()
    if mill:
        now *= 1000
    return int(now)


def datetime_fmt(dt=None, fmt='%Y-%m-%d %H:%M:%S'):
    if isinstance(dt, datetime):
        return dt.strftime(fmt)
    return datetime.now().strftime(fmt)

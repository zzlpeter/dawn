import time


__all__ = ['timestamp']


def timestamp(mill=False):
    now = time.time()
    if mill:
        now *= 1000
    return int(now)

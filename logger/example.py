import traceback
from logger import LoggerPool

other_logger = LoggerPool.other


def test_log():
    try:
        other_logger.info('begin to log')
        1 / 0
    except Exception as e:
        other_logger.error(traceback.format_exc())
        other_logger.error({'exception': traceback.format_exc()})

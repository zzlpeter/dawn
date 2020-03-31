import traceback
from logger import get_logger

other_logger = get_logger('other')


def test_log():
    try:
        other_logger.info('begin to log')
        1 / 0
    except Exception as e:
        other_logger.error(traceback.format_exc())
        other_logger.error({'exception': traceback.format_exc()})

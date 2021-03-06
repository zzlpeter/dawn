import logging
import logging.config
import json
import datetime
from copy import deepcopy

from libs import Host, timestamp, datetime_fmt, singleton
from tomlconfig import Config


REMOVE_ATTR = ["module", "exc_text", "stack_info", "created", "msecs", "relativeCreated", "exc_info"]


class NormalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return datetime_fmt(o)
        return super(NormalEncoder, self).default(o)


class JSONFormatter(logging.Formatter):

    host_ip = Host().host_ip()
    host_name = Host().host_name()

    def format(self, record):
        extra = self.build_record(record)
        # self.format_extra_info(extra)
        self.set_format_time(extra)
        self.set_host_ip(extra)
        extra['args'] = str(extra.get('args', ''))
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(extra, ensure_ascii=False, cls=NormalEncoder)

    @classmethod
    def build_record(cls, record):
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in REMOVE_ATTR
        }

    @classmethod
    def set_format_time(cls, extra):
        now = timestamp()
        extra['timestamp'] = now
        extra['time_fmt'] = datetime_fmt()

    @classmethod
    def format_extra_info(cls, extra):
        # msg = extra.get('msg', {}) or {}
        # base = ['filename', 'lineno', 'function_name', 'log_key']
        # for b in base:
        #     t = msg.pop(b, None)
        #     if t is not None:
        #         extra[b] = t
        # extra['msg'] = msg
        pass

    @classmethod
    def set_host_ip(cls, extra):
        extra['host_name'] = JSONFormatter.host_name
        extra['host_ip'] = JSONFormatter.host_ip


class LoggerConf:
    def __init__(self, basic_conf=None):
        if isinstance(basic_conf, dict):
            self.__basic_conf = basic_conf
        else:
            self.__basic_conf = self.cpy_basic_conf

    @property
    def cpy_basic_conf(self):
        log_conf = {
            # 基本设置
            'version': 1,
            'disable_existing_loggers': False,
            # 日志格式集合
            'formatters': {
                'json': {
                    'class': 'logger.JSONFormatter'
                }
            },
            # 处理器集合(配置文件读取)
            'handlers': {
                # 'root_handler': {
                #     'level': 'DEBUG',
                #     'class': 'logging.handlers.RotatingFileHandler',
                #     'formatter': 'json',
                #     'filename': os.path.join("./log/", 'root.log'),  # 输出位置
                #     'maxBytes': 1024 * 1024 * 5,  # 文件大小 5M
                #     'backupCount': 5,  # 备份份数
                #     'encoding': 'utf8',  # 文件编码
                # },
            },
            # 日志管理器集合(配置文件读取)
            'loggers': {
                # 'root': {
                #     'handlers': ['root_handler'],
                #     'level': 'DEBUG'
                # }
            }
        }
        return deepcopy(log_conf)

    @property
    def cpy_handler(self):
        handler = {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json',
            # 'filename': os.path.join("./log/", 'root.log'),  # 输出位置
            'maxBytes': 1024 * 1024 * 5,  # 文件大小 5M
            'backupCount': 5,  # 备份份数
            'encoding': 'utf8',  # 文件编码
        }
        return deepcopy(handler)

    @property
    def cpy_logger(self):
        logger = {
            'handlers': [],
            'level': 'DEBUG'
        }
        return deepcopy(logger)

    @staticmethod
    def read_toml():
        cnf = Config().logger
        return cnf

    def make_full_conf(self):
        basic = self.__basic_conf
        toml = self.read_toml()
        for handler, conf in toml.items():
            basic_handler = self.cpy_handler
            basic_logger = self.cpy_logger
            basic_handler.update(conf)
            basic_logger['handlers'].append(handler)
            if conf.get('level'):
                basic_logger['level'] = conf['level']
            basic['handlers'][handler] = basic_handler
            basic['loggers'][handler] = basic_logger
        return basic


# 获取logger完整配置
logger_conf = LoggerConf().make_full_conf()
logging.config.dictConfig(logger_conf)


class LoggerWrap:
    def __getattr__(self, key):
        return logging.getLogger(key)


LoggerPool = LoggerWrap()

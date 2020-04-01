import peewee_async

from tomlconfig import Config
from libs import singleton, dict2obj


@singleton
class Engines:
    # 获取MySQL配置信息
    mysql_conf = Config().mysql

    def __init__(self):
        self.engines = dict()
        for alias, cnf in self.mysql_conf.items():
            db = cnf.pop('db')
            is_async = cnf.pop('is_async', False)
            db_conn = peewee_async.PooledMySQLDatabase(db, **cnf)
            # 是否异步操作
            if not bool(is_async):
                db_conn.set_allow_sync(False)
            manager = peewee_async.Manager(db_conn)
            # 每个链接对象有两个属性：.db_conn  .manager
            self.engines[alias] = dict2obj(dict(db_conn=db_conn, manager=manager))

    def get_engine(self, alias):
        if alias not in self.engines:
            raise Exception('alias: <{}> is not found from conf file'.format(alias))
        return self.engines[alias]

    def __getattr__(self, alias):
        return self.get_engine(alias)


EnginesEntity = Engines()


# class AppRouter:
#     @staticmethod
#     def db_for_operation(model):
#         meta = getattr(model, 'Meta')
#         if not meta:
#             raise Exception('model: <{}> not define Meta'.format(model.__name__))
#         db_label = getattr(model.Meta, 'db_label', 'default')
#         return Engines().get_engine(db_label)
#
#
# class BaseModelMix(peewee.Model):
#     @classmethod
#     def manager(cls):
#         db_info = AppRouter.db_for_operation(cls)
#         return db_info['manager']
#
#     @classmethod
#     def db_conn(cls):
#         db_info = AppRouter.db_for_operation(cls)
#         return db_info['db_conn']

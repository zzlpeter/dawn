import peewee

from mysql import MysqlPools


class DouYinUser(peewee.Model):
    id = peewee.IntegerField()
    username = peewee.CharField()
    password = peewee.CharField()

    class Meta:
        database = MysqlPools.default.db_conn
        db_table = 'dy_user'


async def create_user():
    objects = MysqlPools.default.manager
    await objects.create(DouYinUser, username='peter1', password='pwd')

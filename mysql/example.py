import peewee

from mysql import Engines


class DouYinUser(peewee.Model):
    id = peewee.IntegerField()
    username = peewee.CharField()
    password = peewee.CharField()

    class Meta:
        database = Engines().default.db_conn
        db_table = 'dy_user'


async def create_user():
    objects = Engines().default.manager
    await objects.create(DouYinUser, username='peter1', password='pwd')

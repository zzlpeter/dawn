from mysql import Engines
import peewee
import asyncio


class DouYinUser(peewee.Model):
    id = peewee.IntegerField()
    username = peewee.CharField()
    password = peewee.CharField()

    class Meta:
        database = Engines().default.db_conn
        db_table = 'dy_user'
        # manager =

async def test():
    objects = Engines().default.manager
    await objects.create(DouYinUser, username='peter1', password='pwd')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()

# -*- coding: utf-8 -*-

import datetime

from peewee import *

db = SqliteDatabase('statistics.db')


# 文章表
class Models(Model):
    _id = PrimaryKeyField
    id = CharField()  # 模型id
    name = CharField()  # 模型名称
    runCount = IntegerField(default=0, null=False)
    downloadCount = IntegerField(default=0, null=False)
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db


def delete_table():
    return Models.delete().execute()


def init_table():
    db.connect()
    db.create_tables([Models])


if __name__ == '__main__':
    init_table()

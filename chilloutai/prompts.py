# -*- coding: utf-8 -*-

import datetime
from peewee import *

db = SqliteDatabase('chilloutai.db')


class Chilloutai(Model):
    id = CharField(primary_key=True)
    seed = CharField(null=True)
    steps = CharField(null=True)
    width = CharField(null=True)
    height = CharField(null=True)
    prompt = TextField(null=True)
    negative_prompt = TextField(null=True)
    batch_size = CharField(null=True)
    sampler_index = CharField()
    image_url = CharField()
    cfg_scale = CharField(null=True)
    grabState = IntegerField(default=0, null=False)# 抓取状态
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db  # This model uses the "people.db" database.


def delete_prompt():
    return Chilloutai.delete().execute()


def init_table():
    db.connect()
    db.create_tables([Chilloutai])


if __name__ == '__main__':
    db.connect()
    db.create_tables([Chilloutai])

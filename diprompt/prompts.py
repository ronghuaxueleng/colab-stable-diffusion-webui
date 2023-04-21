# -*- coding: utf-8 -*-

import datetime
from peewee import *

db = SqliteDatabase('prompts.db')


class Prompt(Model):
    _id = CharField(primary_key=True)
    imageId = CharField()
    url = CharField()
    width = CharField(null=True)
    height = CharField(null=True)
    tags = TextField(null=True)
    promptText = TextField()
    negativePromptText = TextField()
    text = TextField()
    model = IntegerField()
    samplingMethod = CharField()
    samplingSteps = CharField()
    cfgScale = CharField()
    viewCount = CharField()
    step = CharField()
    state = CharField()
    createdTime = DateTimeField()
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db  # This model uses the "people.db" database.


def delete_prompt():
    return Prompt.delete().execute()


def init_table():
    db.connect()
    db.create_tables([Prompt])


if __name__ == '__main__':
    db.connect()
    db.create_tables([Prompt])

#_*_ coding: UTF8 _*_
from peewee import SqliteDatabase
from peewee import Model

DATABASE = SqliteDatabase('melk.db')

class BaseModel(Model):
    class Meta:
        database = DATABASE

    def __eq__(self, other):
        return self.__dict__.get('_data') == other.__dict__.get('_data')

    def set(self, kwargs):
        self.__dict__.get('_data').update(kwargs)
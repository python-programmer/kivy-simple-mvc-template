#_*_ coding: UTF8 _*_
from peewee import (PrimaryKeyField, IntegerField, TextField, ForeignKeyField)
from .base import BaseModel
from Model.feature import Feature


class Service(BaseModel):
    id = PrimaryKeyField()
    type = IntegerField()
    description = TextField(null = True)
    feature = ForeignKeyField(Feature, related_name = 'services', null = True)

    def __unicode__(self):
        return self.type

    def __eq__(self, other):
        # self filled by json dictionary and not exists in database. as
        # self.__dict__.get('_data').update(kwargs) is used for fill them
        # and in the kwargs we haven't feature attribute thus self haven't this attribute
        _ = self.__dict__.get('_data')
        __ = other.__dict__.get('_data')
        del __['feature']
        return _ == __
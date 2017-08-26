#_*_ coding: UTF8 _*_
from peewee import (PrimaryKeyField, IntegerField, BooleanField, TextField,
    ForeignKeyField, CharField)
from .base import BaseModel
from .services import Service


class Images(BaseModel):
    id = PrimaryKeyField()
    file_name = CharField(max_length = 128)
    is_default = BooleanField(default = False)
    service = ForeignKeyField(Service, related_name = 'images', null = True)

    def __unicode__(self):
        return self.is_default

    def __eq__(self, other):
        _ = other.__dict__.get('_data')
        del _['service']
        return self.__dict__.get('_data') == _
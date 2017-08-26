#_*_ coding: UTF8 _*_
from .base import BaseModel
from peewee import PrimaryKeyField, CharField

class Address(BaseModel):
    id = PrimaryKeyField()
    country = CharField(max_length = 64)
    province = CharField(max_length = 64)
    city = CharField(max_length = 64)
    region = CharField(max_length = 64, null = True)
    postal_code = CharField(max_length = 64, null = True)
    addr = CharField(max_length = 200)

    def __unicode__(self):
        return self.addr
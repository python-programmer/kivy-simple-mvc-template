#_*_ coding: UTF8 _*_
from peewee import (PrimaryKeyField, IntegerField, CharField,
    BooleanField)
from .base import BaseModel


class User(BaseModel):
    id = PrimaryKeyField(null = True)
    username = CharField(max_length = 32)
    first_name = CharField(max_length = 64, null = True)
    last_name = CharField(max_length = 64, null = True)
    password = CharField(max_length = 64, null = True)
    image_url = CharField(max_length = 200, null = True)

    country = CharField(max_length = 128, null = True)
    province = CharField(max_length = 128, null = True)
    city = CharField(max_length = 128, null = True)
    region = CharField(max_length = 128, null = True)
    postal_code = CharField(max_length = 32, null = True)
    addr = CharField(max_length = 200, null = True)

    city_code = IntegerField(null = True)
    tel = IntegerField(null = True)

    is_active = BooleanField(default = False)

    def __unicode__(self):
        return self.username
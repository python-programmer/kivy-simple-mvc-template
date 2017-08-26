#_*_ coding: UTF8 _*_
from peewee import (PrimaryKeyField, IntegerField)
from .base import BaseModel


class Home(BaseModel):
    id = PrimaryKeyField()
    frame_type = IntegerField(default = 0)
    floor = IntegerField(default = 0)
    the_floor = IntegerField(default = 0)
    unit = IntegerField(default = 0)

    def __unicode__(self):
        return '{} floor is {}'.format(self.frame_type, self.floor)
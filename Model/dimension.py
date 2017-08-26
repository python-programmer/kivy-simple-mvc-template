#_*_ coding: UTF8 _*_
from .base import BaseModel
from peewee import PrimaryKeyField, FloatField

class Dimension(BaseModel):
    id = PrimaryKeyField()
    height = FloatField()
    width = FloatField()

    def __unicode__(self):
        return '{0} X {1}'.format(self.width, self.height)
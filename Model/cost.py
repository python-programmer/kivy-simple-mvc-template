#_*_ coding: UTF8 _*_
from .base import BaseModel
from peewee import PrimaryKeyField, BigIntegerField

class Cost(BaseModel):
    id = PrimaryKeyField()
    cost_metric = BigIntegerField()
    price = BigIntegerField()

    def __unicode__(self):
        return self.price
    

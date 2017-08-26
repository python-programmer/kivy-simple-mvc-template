#_*_ coding: UTF8 _*_
from peewee import (PrimaryKeyField, IntegerField, BooleanField)
from .base import BaseModel

class Facilities(BaseModel):
    id = PrimaryKeyField()
    bedroom = IntegerField(default = 0)
    heating_system = BooleanField(default = False)
    cooling_system = BooleanField(default = False)
    well = BooleanField(default = False)
    warehouse = BooleanField(default = False)
    basement = BooleanField(default = False)
    elevator = BooleanField(default = False)
    balcony = BooleanField(default = False)
    shooting = BooleanField(default = False)

    def __unicode__(self):
        return self.bedroom
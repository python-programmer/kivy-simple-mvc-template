#_*_ coding: UTF8 _*_
from peewee import (PrimaryKeyField, IntegerField, BooleanField, TextField,
    ForeignKeyField)
from .base import BaseModel
from .address import Address
from .cost import Cost
from .dimension import Dimension
from .experience import Experience
from Model.facilities import Facilities
from Model.user import User
from Model.home import Home


class Feature(BaseModel):
    id = PrimaryKeyField()
    type = IntegerField(default = 0)
    priority = IntegerField(default = 1)
    situation = BooleanField(default = False) # True => Sell and False => Rent
    document = IntegerField(default = 0)
    position = IntegerField(default = 0)
    area = IntegerField()
    built_up_area = IntegerField()
    control = IntegerField(default = 0)
    construction_date = IntegerField(default = 1300)
    description = TextField()
    is_show = BooleanField(default = False)
    is_sold = BooleanField(default = False)

    address = ForeignKeyField(Address, related_name = 'feature', null = True)
    cost = ForeignKeyField(Cost, related_name = 'feature', null = True)
    dimension = ForeignKeyField(Dimension, related_name = 'feature', null = True)
    experience = ForeignKeyField(Experience, related_name = 'feature', null = True)
    facilities = ForeignKeyField(Facilities, related_name = 'feature', null = True)
    home = ForeignKeyField(Home, related_name = 'feature', null = True)
    user = ForeignKeyField(User, related_name = 'feature', null = True)

    def __unicode__(self):
        return '{0} and area {1}'.format(self.type, self.area)

    def __eq__(self, other):
        _ = other.__dict__.get('_data').copy()
        __ = self.__dict__.get('_data').copy()
        del _['address'], _['cost'], _['dimension'], _['experience'], _['facilities'], _['home'], _['user']
        return _ == __
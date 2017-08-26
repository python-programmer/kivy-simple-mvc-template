#_*_ coding: UTF8 _*_
from .base import BaseModel
from peewee import PrimaryKeyField, BooleanField

class Experience(BaseModel):
    id = PrimaryKeyField()
    water = BooleanField(default = False)
    power = BooleanField(default = False)
    phone = BooleanField(default = False)
    gas = BooleanField(default = False)

    def __unicode__(self):
        return 'water {0}, power {1}, phone {2}, gas {3}'.format(self.water,
                                                                 self.power,
                                                                 self.phone,
                                                                 self.gas)
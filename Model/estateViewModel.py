# _*_ coding: UTF8 _*_
from Model.base import BaseModel
from peewee import PrimaryKeyField, IntegerField, BooleanField, CharField

WEBSITE = "http://localhost:8888"
ESTATETYPE = [u'نامشخص',
               u'خانه',
               u'آپارتمان',
               u'زمین',
               u'تجاری']

SITUATION = [u'فروش',
              u'رهن']


class EstateViewModel(BaseModel):
    id = PrimaryKeyField()
    priority = IntegerField(default = 1)
    type = IntegerField(default = 1)
    sell_or_rent = BooleanField(default = False)
    area = IntegerField()
    price = IntegerField()
    image_url = CharField(max_length=128)
    is_sold = BooleanField(default = False)
    bedroom = IntegerField()

    def get_image_url(self):
        #return ''.join([WEBSITE, self.image_url])
        return self.image_url

    def get_estate_type(self):
        return u' [color=000]-[/color] '.join([ESTATETYPE[self.type], self.get_situation()])

    def get_situation(self):
        return SITUATION[self.sell_or_rent]

    def get_price(self):
        _ = u'[color=000]:اجاره [/color]' if self.sell_or_rent else u'[color=000]:قیمت [/color]'
        __ = u'[color=000] تومان[/color]'
        return ' '.join([__, str(self.price), _])

    def get_area(self):
        _ = u'[color=000]:مساحت [/color]'
        __ = u'[color=000] مترمربع[/color]'
        return ' '.join([__, str(self.area), _])
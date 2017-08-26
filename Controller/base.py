#_*_ coding: UTF8 _*_
from peewee import IntegrityError

class BaseOperation(object):

    def add(self, Object, items):
        try:
            object_client = Object.create(**items)
        except IntegrityError:
            object_client = Object.get(Object.id == items['id'])
            object_server = Object()
            object_server.set(items)
            if object_server != object_client:
                self.update(Object, items)
        return object_client

    def update(self, Object, item):
        Object.update(**item)\
                            .where(Object.id == item['id'])\
                            .execute()
#_*_ coding: UTF8 _*_
from Model.services import Service
from Controller.images import ImageOperation
from Controller.base import BaseOperation
from peewee import IntegrityError

image_operation = ImageOperation()

class ServiceOperation(BaseOperation):
    
    def add(self, service, feature):
        items = service.copy()
        del items['images']

        serv = super(ServiceOperation, self).add(Service, items)
        serv.feature = feature
        serv.save()

        self.add_images(service.get('images'), serv)
        return serv

    def add_images(self, images, service):
        for image in images:
            image = image_operation.add(image, service)

    
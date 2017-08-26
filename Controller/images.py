#_coding: UTF8 _*_
from Model.images import Images
from Model import get_image
from peewee import IntegrityError
from Controller.base import BaseOperation

class ImageOperation(BaseOperation):
    
    def add(self, image, service):
        if image.get('file_name'):
            image['file_name'] = get_image(image['file_name'], 'images/services/')

        img = super(ImageOperation, self).add(Images, image)
        img.service = service
        img.save()

        return img
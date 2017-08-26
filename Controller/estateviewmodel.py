# _*_ coding: UTF8 _*_
from Model.estateViewModel import EstateViewModel
from Model import get_image, get_local_filename
from Model.base import DATABASE
from peewee import IntegrityError
from Controller.base import BaseOperation


class EstateOperation(BaseOperation):

    def add(self, records):
        estate_list =[]
        for item in records:
            item['image_url'] = get_image(item.get('image_url'))
            estate = super(EstateOperation, self).add(EstateViewModel, item)
            estate_list.append(estate)

        #FIXME: if data on server and client is same must return local data
        #FIXED: if return data from add method is empty system call restore_local_data       
        return estate_list

    def index(self):
        return EstateViewModel.select()
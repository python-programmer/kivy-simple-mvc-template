#_*_ coding: UTF8 _*_
from Model.feature import Feature
from Controller.home import HomeOperation
from Controller.address import AddressOperation
from Controller.cost import CostOperation
from Controller.dimension import DimensionOperation
from Controller.experience import ExperienceOperation
from Controller.facilities import FacilitiesOperation
from Controller.user import UserOperation
from Controller.services import ServiceOperation
from Model.facilities import Facilities
from Model.address import Address
from Model.cost import Cost
from Model.dimension import Dimension
from Model.experience import Experience
from Model.home import Home
from Model.user import User
from Controller.base import BaseOperation

home_operation = HomeOperation()
address_operation = AddressOperation()
cost_operation = CostOperation()
dimension_operation = DimensionOperation()
experience_operation = ExperienceOperation()
facilities_operation = FacilitiesOperation()
user_operation = UserOperation()
service_operation = ServiceOperation()

class FeatureOperation(BaseOperation):
    
    def add(self, melk):
        feature = super(FeatureOperation, self).add(Feature, melk['feature'])
        self.add_other_attributes(melk, feature)
        return feature

    def add_other_attributes(self, melk, feature):
        if melk.get('address'):
            address = address_operation.add(Address, melk.get('address'))
            feature.address = address
        if melk.get('cost'):
            cost = cost_operation.add(Cost, melk.get('cost'))
            feature.cost = cost
        if melk.get('dimension'):
            dimension = dimension_operation.add(Dimension, melk.get('dimension'))
            feature.dimension = dimension
        if melk.get('experience'):
            experience = experience_operation.add(Experience, melk.get('experience'))
            feature.experience = experience
        if melk.get('facilities'):
            facilities = facilities_operation.add(Facilities, melk.get('facilities'))
            feature.facilities = facilities
        if melk.get('home'):
            home = home_operation.add(Home, melk.get('home'))
            feature.home = home
        if melk.get('services'):
            for service in melk.get('services'):
                service_operation.add(service, feature)
        if melk.get('user'):
            user = user_operation.add(User, melk.get('user'))
            feature.user = user
        feature.save()

    def __getitem__(self, index):
        try:
            return Feature.get(Feature.id == index)
        except:
            return None
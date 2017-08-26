# _*_ coding: UTF8 _*_
import kivy
from Controller.feature import FeatureOperation
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import AccordionItem
from requests import get, ConnectionError
from kivy.properties import (ObjectProperty, StringProperty, NumericProperty, ListProperty)
from kivy.network.urlrequest import UrlRequest
from kivy.factory import Factory
from Model import estateViewModel, initial_db
from bidi.algorithm import get_display
import arabic_reshaper
#from Model import store, get
from Controller.estateviewmodel import EstateOperation

base_url = ''.join([estateViewModel.WEBSITE, '/real-estate/?page={}'])
detail_url = '/'.join([estateViewModel.WEBSITE, 'real-estate/{}'])
PAGE_SIZE = 4.0
MAXHEIGHT = 768
MELKITEMHEIGHT = 100
STRINGEMPTY = ''
estate_operation = EstateOperation()
feature_operation = FeatureOperation()


def set_shape(text):

    if isinstance(text, str):
        text = unicode(text, 'utf-8')

    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class Loading(BoxLayout):

    def __init__(self, **kwargs):
        super(Loading, self).__init__(**kwargs)
        self.padding = '7dp'
        self.orientation = 'vertical'
        loading_image = Image(source = 'data/images/loading.gif')
        self.add_widget(loading_image)

LOADING = Popup(title = 'Loading ...', content = Loading(), size_hint = (None, None), size = ('169dp', '144dp'))

def restore_data(url, success_func, failure_func):
    progress_start()
    try:
        response = get(url)
        if response.status_code == 200:
            success_func(response.json())
        else:
            failure_func([])
    except ConnectionError:
        failure_func([])
    progress_end()
  
def progress_start():
    LOADING.open()
 
def progress_end():
    LOADING.dismiss()

class UnicodeLabel(Label):
    def __init__(self, **kwargs):
        self.font_name = 'data/fonts/Mirta.ttf'
        self.markup = True
        self.color = (1, 0, 0.96, 1)
        super(UnicodeLabel, self).__init__()

    def set_shape(self, text):
    
        if isinstance(text, str):
            text = unicode(text, 'utf-8')

        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

#    RuntimeError: maximum recursion depth exceeded
#    def on_text(self, *args):
#        self.text = self.set_shape(args[1])

class Index(BoxLayout):
    estates = ObjectProperty()
    scroll_view = ObjectProperty()
    page = 1
    count = 0
    lock = False

    def search_operation(self, url = base_url):
        self.lock = True
        restore_data(url, self.restore_data, self.restore_local_data)

    def restore_data(self, data):
        # if first UrlRequest failure and after restore_local_data
        # UrlRequest success, all previous data cleared from screen
        if self.page is 1:
            self.estates.clear_widgets()

        self.get_data(data)
        if len(data):
            scroll_y = (1.0/self.page)*(len(data)/PAGE_SIZE)
            self.count += len(data)

            # set scroll to point that data added
            self.scroll_view.scroll_y = scroll_y
            self.page += 1
 
        self.lock = False
        if len(data) and (MAXHEIGHT >= (self.count * MELKITEMHEIGHT)):
            url = base_url.format(self.page)
            self.search_operation(url)

    def get_data(self, data):
        estate_list = estate_operation.add(data)
        if estate_list:
            self.set_melk_items(estate_list)
        else:
            self.restore_local_data()
        

    def set_melk_items(self, estate_list):
        for estate in estate_list:
            melk_item = MelkItem()
            self.set_melk_item(melk_item, estate)
            self.estates.add_widget(melk_item)

    def restore_local_data(self, *args):
        if not self.estates.children:
            estate_list = estate_operation.index()
            self.set_melk_items(estate_list)
        self.lock = False

    def set_melk_item(self, melk_item, melk):
        """
        @type melk: EstateViewModel 
        """
        melk_item.melk_id = melk.id
        melk_item.area = melk.get_area()
        melk_item.price = melk.get_price()
        melk_item.type = melk.get_estate_type()
        melk_item.image_url = melk.get_image_url()

    def scrolling(self, scroll_y):
        if scroll_y <= 0.0 and self.lock is False:
            url = base_url.format(self.page)
            self.search_operation(url)
            

class MelkItem(BoxLayout):
    melk_id = NumericProperty()
    type = StringProperty()
    area = StringProperty()
    price = StringProperty()
    image_url = StringProperty()
    background_color = ListProperty([1, 1, 1])

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.background_color = [0.95, 0.95, 0.95]
        return super(MelkItem, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        touch.ud['melk_item'] = True
        self.background_color = [1, 1, 1]
        super(MelkItem, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        # if touch moved don't response to them just touch up
        if touch.ud.get('melk_item') is None:
            if self.collide_point(touch.x, touch.y):
                self.background_color = [1, 1, 1]
                self.show()
        else:
            touch.ud['melk_item'] = False
        super(MelkItem, self).on_touch_up(touch)

    def show(self):
        app = MelkApp.get_running_app()
        app.root.show(self.melk_id)

class Melk(BoxLayout):
    pass

class RealEstateContainer(BoxLayout):
    index_page = ObjectProperty()
    melk_page = ObjectProperty(None)
    container_view = ObjectProperty()

    def __init__(self, **kwargs):
        self.font_name = 'data/fonts/Mirta.ttf'
        super(RealEstateContainer, self).__init__(**kwargs)
        self.index_page.search_operation()

    def show(self, melk_id):
        url = detail_url.format(melk_id)
        self.melk_page = Melk()
        self.feature = feature_operation[melk_id]
        if self.feature is None:
            restore_data(url, self.get_melk, self.get_melk)
        if self.feature is not None:
            self.show_melk()
        self.container_view.clear_widgets()
        self.container_view.add_widget(self.melk_page)

    def show_latest_view_melk(self):
        if self.melk_page is not None:
            self.container_view.clear_widgets()
            self.container_view.add_widget(self.melk_page)

    def get_melk(self, data):
        if data:
            data = data[0]
            self.feature = feature_operation.add(data)

    def show_index(self):
        self.container_view.clear_widgets()
        self.container_view.add_widget(self.index_page)

    def show_melk(self):
        _ = self.feature
        feature = self.melk_page.ids.feature
        feature.area = _.area
        feature.built_up_area = _.built_up_area
        feature.construction_date = _.construction_date
        feature.control = str(_.control)
        feature.document_situation = str(_.document)
        feature.estate_position = str(_.position)
        feature.estate_type = str(_.type)
        feature.estate_priority = str(_.priority)
        feature.description = _.description or STRINGEMPTY
        feature.is_sold = _.is_sold
        
        if _.home:
            home = self.melk_page.ids.home
            home.frame_type = str(_.home.frame_type)
            home.number_of_floors = _.home.floor
            home.floor_for_sell_or_rent = _.home.the_floor
            home.unit_for_sell_or_rent = _.home.unit
        
        if _.experience:
            experience = self.melk_page.ids.experience
            experience.water = _.experience.water
            experience.power = _.experience.power
            experience.phone = _.experience.phone
            experience.gas = _.experience.gas
        
        if _.facilities:
            facilities = self.melk_page.ids.facilities
            facilities.number_of_bedrooms = _.facilities.bedroom
            facilities.heating_system = _.facilities.heating_system
            facilities.cooling_system = _.facilities.cooling_system
            facilities.well = _.facilities.well
            facilities.warehouse = _.facilities.warehouse
            facilities.balcony = _.facilities.balcony
            facilities.basement = _.facilities.basement
            facilities.elevator = _.facilities.elevator
            facilities.shooting = _.facilities.shooting
        
        if _.services:
            service = self.melk_page.ids.service
            for item in _.services:
                serv = AccordionItem(title=str(item.type))
                 
                srv = Factory.Service()
                srv.description = item.description or STRINGEMPTY
        
                for image in item.images:
                    __ = Factory.EstateImage()
                    __.is_default = image.is_default
                    __.file_name = image.file_name
                    srv.add_widget(__)
        
                serv.add_widget(srv)
                service.add_widget(serv)
        
        description = self.melk_page.ids.description
        description.description = feature.description
        
        if _.address:
            address = self.melk_page.ids.address
            address.country = _.address.country or STRINGEMPTY
            address.province = _.address.province or STRINGEMPTY
            address.city = _.address.city or STRINGEMPTY
            address.region = _.address.region or STRINGEMPTY
            address.address = _.address.addr or STRINGEMPTY
            address.postal_code = _.address.postal_code or STRINGEMPTY
        
        if _.cost:
            cost = self.melk_page.ids.cost
            cost.cost_metric = _.cost.cost_metric
            cost.price = _.cost.price
        
        if _.user:
            user = self.melk_page.ids.user
            user.first_name = _.user.first_name or STRINGEMPTY
            user.last_name = _.user.last_name or STRINGEMPTY
            user.mobile_number = ''.join(['09', str(_.user.username)]) or STRINGEMPTY
            user.phone_number = ''.join(['0', str(_.user.city_code), ' - ', str(_.user.tel)]) or STRINGEMPTY

class DetailGrid(GridLayout):
    def __init__(self, **kwargs):
        super(DetailGrid, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))

class ScrollContainer(GridLayout):
    def __init__(self, **kwargs):
        super(ScrollContainer, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        
class MelkApp(App):
    pass

if __name__ == '__main__':
    # Initialize database for models
    initial_db()
    MelkApp().run()
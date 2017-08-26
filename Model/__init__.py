import requests
import shutil
import os

from . import estateViewModel
from .base import DATABASE
import Model

def get_image(file_name, local_dir = 'images/estates/'):
    response = requests.get(''.join([estateViewModel.WEBSITE, file_name]), stream = True)
    if response.status_code == 200:
        local_filename = get_local_filename(file_name, local_dir)
        with open(local_filename, 'wb') as image_file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, image_file)
    return local_filename

def get_local_filename(file_name, local_dir):
    _ = file_name.split('/')
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    local_filename = '/'.join([local_dir, _[-1]])
    return local_filename

def initial_db():
    models = get_models()
    DATABASE.connect()
    DATABASE.create_tables(models, safe=True)

def get_models(base_class = Model.base.BaseModel):
    import inspect
    import importlib
    models = []
    files = get_files()

    for file in files:
        module = importlib.import_module(file)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and (obj is not base_class) and issubclass(obj, base_class):
                models.append(obj)
    return models


def get_files(module_path = os.path.dirname(__file__), package = 'Model'):
    files = []
    for file in os.listdir(module_path):
        module, extension = os.path.splitext(file)
        if os.path.isfile(os.path.join(module_path,file)) and extension == '.py':
                files.append('.'.join([package, module]))
    return files
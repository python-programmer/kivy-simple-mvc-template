# kivy-simple-mvc-template
simple mvc starter template

This app is made for a real estate web service, Kivy is used to implement it. This project uses MVC pattern, Which can be a starter template to start working with the kivy.

This project uses peewee as a ORM, And SQLite as database engine.

Firstly, app will get real estates from the Web service and, if it has new real estates, it will store new real estates info in the database.

## Requirements

* [Python 2.7](https://www.python.org/downloads/release/python-2712/)
* [Kivy](https://kivy.org/#home)
* [Pillow](https://python-pillow.org/)
* [PyGame](https://www.pygame.org/news)
* [Python-bidi](https://pypi.python.org/pypi/python-bidi)
* [PeeWee](https://github.com/coleifer/peewee)

## Kivy Installation

Install Kivy via the [this](https://kivy.org/#download) link

please refer to the installation instructions for your specific platform

> To install a kivy package, we recommend using the virtualenv tool

## Install other requirements
In the root directory of project, run below code in terminal

`pip install -r requirements.txt`

## Run the project
In the root directory of project, run below code in terminal

`python main.py`

## Packaging the application
Using [this](https://kivy.org/docs/guide/packaging.html) link for packaging the application for Win, Mac, iOS, Android Platforms

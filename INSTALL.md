## Dependencies

DoTS should run on any OS that can run Django 1.4.x.
It was tested on current version of Arch Linux

* Python 2.7.x or 2.6.x
* Django 1.4.x or 1.5.x
* OpenBabel 2.3.x with Python bindings (OpenBabel also needs cairo library)
* Numpy 1.7.x
* Any database supported by Django (with python bindings)
* Any web server that can run Django (with wsgi support)

## Installation

`git clone https://github.com/samoturk/openmolDB.github`

Then deploy it as you would any other Django project.

Set servername variable in openmoldb/views.py to the name of your server.
Have a look at settings.py and set your database engine, time zone, etc.




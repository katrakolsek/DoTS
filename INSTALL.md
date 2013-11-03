## Dependencies

DoTS should run on any OS that can run Django 1.4.x.
It was tested on current version of Arch Linux

* Python 2.7.x or 2.6.x
* Django 1.4.x or 1.5.x
* OpenBabel 2.3.x with Python bindings (OpenBabel also needs cairo library)
* Numpy 1.7.x
* Celery and django-celery 3.0.x (with associated dependencies)
* RabbitMQ or any other messaging system compatible with celery
* Any database supported by Django (with python bindings)
* Any web server that can run Django (with wsgi support)

## Installation

`git clone https://github.com/katrakolsek/DoTS.git`

Then deploy it as you would any other Django project.

Have a look at settings.py and set your database engine, time zone, etc.

## Running development server

Start the server:
`python2 manage.py runserver`

Start Celery worker:
`python2 manage.py celery worker --loglevel=info`

## Do not forget when deploying

* Set debug to false
* Replace SECRET_KEY
* Change ALLOWED_HOSTS to your host
* Change admin (katra) password (default=test)


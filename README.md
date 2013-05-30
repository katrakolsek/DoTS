DoTS
============

Docking interface for Target Systems

![Editor Screenshot](https://raw.github.com/katrakolsek/DoTS/master/DoTS_result.png)

## About

DoTS is open source Docking interface for Target Systems, used for docking 1 molecule to multiple targets
It supports SMILES and structure draw docking with AutoDock Vina.

This project wouldn't be possible without these excellent open source projects:
* Django - Python web framework, which is a base for DoTS
* OpenBabel/pybel - chemistry toolkit with python bindings
* jQuery - javascript library
* AutoDock Vina- suite of automated docking tools
* Celery and django-celery for async tasks (docking in background)
* RabbitMQ - messaging system
* ChemDoodle Web - javascript chemical library, which handles the displayand drawing of chemical structures
* Flot - jQuery plugin for plotting
* Twitter Bootstrap - CSS style
* Font Awesome


## What does not work
* Can crash if can't dock a compound in one of receptors

## Credits

DoTS is developed by Katra Kolšek and Samo Turk.

## Copyright

Copyright 2013 Katra Kolšek and Samo Turk


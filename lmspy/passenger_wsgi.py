 
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/d/django17/django17.beget.tech/HelloDjango')
sys.path.insert(1, '/home/d/django17/django17.beget.tech/venv_django/lib/python3.6/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lmshop.settings.prod_msql'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

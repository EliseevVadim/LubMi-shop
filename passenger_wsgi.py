 
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/g/goodiets/lubmi.ru/lmspy/lmshop')
sys.path.insert(1, '/home/g/goodiets/.local/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lmshop.settings.prod_msql'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

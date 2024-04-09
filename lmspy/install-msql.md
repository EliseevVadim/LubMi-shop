Установка
=========

0. Убедиться, что в использующемся python-окружении доступны пакеты, перечисленные в файле requirements.txt При необходимости их можно установить:
	> pip install -r requirements.txt

0. В файле lmshop/settings/prod_msql.py меняем
	> CSRF_TRUSTED_ORIGINS = ['http://192.168.0.100/*']
	
	на
	
	> CSRF_TRUSTED_ORIGINS = ['http://<_host_>/*']
	
	Это позволит заходить в админку по адресу `http://<host>/admin`.  
0. В том же файле указываем параметры `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` для подключения к БД MySQL|MariaDB
0. Указываем адрес перехода на сайт из админки: в файле lmshop/settings/prod.py меняем
	> SITE_URL = "http://192.168.0.100/lms/"
	
	на
	
	> SITE_URL = "<_site-url_>"
0. Из каталога `lmshop` с файлом `manage.py` запускаем
	> ./manage.py migrate --skip-checks --settings lmshop.settings.prod_msql  
	> ./manage.py loaddata lms.json --settings lmshop.settings.prod_msql  
	> ./manage.py createsuperuser --settings lmshop.settings.prod_msql  
	> env DJANGO_SETTINGS_MODULE=lmshop.settings.prod_msql gunicorn --bind=address:port lmshop.wsgi  
	Для запуска в режиме демона указываем ключ -D:  
	> env DJANGO_SETTINGS_MODULE=lmshop.settings.prod_msql gunicorn --bind=address:port -D lmshop.wsgi  


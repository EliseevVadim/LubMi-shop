Установка
=========
0. Для тестовой установки в файле lmshop/settings/prod.py меняем
	> CSRF_TRUSTED_ORIGINS = ['http://192.168.0.100/*']
	
	на
	
	> CSRF_TRUSTED_ORIGINS = ['http://<_test-host-ip_>/*']
	
	Это позволит заходить в админку по адресу `http://<test-host-ip>/admin`.  
	Установка  
	> DEBUG = True  
	
	включает расширенную диагностику.
0. Указываем адрес перехода на сайт из админки: в файле lmshop/settings/prod.py меняем
	> SITE_URL = "http://192.168.0.100/lms/"
	
	на
	
	> SITE_URL = "<_site-url_>"
0. Из каталога с файлом docker-compose.yaml запускаем
	> docker-compose up -d
0. После запуска магазина последовательно выполняем:
	> docker-compose exec web python manage.py migrate --skip-checks  
	> docker-compose exec web python manage.py loaddata lms.json  
	> docker-compose exec web python manage.py createsuperuser
0. Открываем _http://localhost/lms_
0. Админка: _http://localhost/admin_


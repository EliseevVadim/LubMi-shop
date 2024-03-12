Установка
=========
0. Для тестовой установки в файле lmshop/settings/prod.py меняем
	> CSRF_TRUSTED_ORIGINS = ['http://192.168.0.100/*']
	
	на
	
	> CSRF_TRUSTED_ORIGINS = ['http://<*test-host-ip*\>/*']
	
	Это позволит заходить в админку по адресу `http://<test-host-ip>/admin`.  
	Установка  
	> DEBUG = True  
	
	включает расширенную диагностику.
	
1. Из каталога с файлом docker-compose.yaml запускаем
	> docker-compose up -d
2. После запуска магазина последовательно выполняем:
	> docker-compose exec web python manage.py migrate --skip-checks  
	> docker-compose exec web python manage.py loaddata lms.json  
	> docker-compose exec web python manage.py createsuperuser
3. Открываем _http://localhost/lms_
4. Админка: _http://localhost/admin_


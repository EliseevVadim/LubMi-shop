Установка
=========
1. Из каталога с файлом docker-compose.yaml запускаем
	> docker-compose up -d
2. После запуска магазина последовательно выполняем:
	> docker-compose exec web python manage.py migrate --skip-checks  
	> docker-compose exec web python manage.py loaddata lms.json  
	> docker-compose exec web python manage.py createsuperuser
3. Открываем _http://localhost/lms_
4. Админка: _http://localhost/admin_


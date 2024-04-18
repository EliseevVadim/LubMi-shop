Установка на Beget
==================

0. Убедиться, что в использующемся python-окружении доступны пакеты, перечисленные в файле requirements.txt При необходимости их можно установить:
	> pip install -r requirements.txt
0. Из каталога `lmshop` с файлом `manage.py` запускаем
	> ./manage.py migrate --skip-checks --settings lmshop.settings.prod_beget  
	> ./manage.py loaddata lms.json --settings lmshop.settings.prod_beget  
	> ./manage.py createsuperuser --settings lmshop.settings.prod_beget  


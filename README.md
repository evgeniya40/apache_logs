# apache_logs

Парсинг полученного по ссылке файла логов Apache  заданного формата.
=====================================================================

Осуществляется командой:    

   python3 manage.py link_processing http://www.almhuette-raith.at/apache-log/access.log  
   
Реализация команды находится в link_parser/LinkData/management/commands/link_processing.py.  

Создана модель LinkData с соответствующими полями, которая описывает распарсенные данные из лога.

Используется база Oracle. 

Добавлены тесты, которые (для примера) запускаются следующей командой:

   python3 ./manage.py test LinkData.tests.TestLinkData.test_reg_exp -v3

Добавленные в базу данные отображаются в django-админке. Для просмотра выполнялась команда запуска сервера:

   python3 ./manage.py runserver

Панель django-админ доступна для суперпользователей по ссылке 127.0.0.1:8000/admin/. 

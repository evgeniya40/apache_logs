'''
В составе приложения должна быть Management command,
которая на вход принимает ссылку на лог файл определенного формата, скачивает ее, парсит и записывает в БД.
'''

from django.core.management.base import BaseCommand
from LinkData.models import LinkData
import requests
import re

class Command(BaseCommand):
    '''
    Объект команды для парсинга логов по ссылке.
    Команда принимает на вход аргумет - ссылку на файл лога, который загружает, например,
    python3 manage.py link_processing http://www.almhuette-raith.at/apache-log/access.log
    '''

    help = u''

    def log_parser(self, log_str):
        '''
        Функция записи данных из Apache лога в БД.
        :param log_str: строка лога
        '''
        regex = '([(\w\.))]+) - (-|adva) \[(.*?)\] "(.*?)" (\d+) (\d+|-) "(.*?)" "(.*?)" "-"'
        if re.match(regex, log_str) is None:
                print("Error! Line does not match the format!Skipping.....")
                return False
        else:
            try:
                print("Parsing next line...")
                data_line = re.match(regex, log_str).groups()
                #форматируем значение даты, чтобы не выводилось ничего лишнего, кроме ДД/ММ/ГГГГ
                date = data_line[2].split(' ')[0]
                ind = date.index(':')
                date = str(date[:ind])
                new_el = LinkData(ip=data_line[0],
                                  date=str(date),
                                  http_method=data_line[3].split(' ')[0],
                                  uri=data_line[3].split(' ')[1],
                                  response_code=str(data_line[4]),
                                  size=str(data_line[5]))
                new_el.save()
                print("saved")
            except:
                print("Line could not be loaded. Skipping.....")
                return False
        return True

    def add_arguments(self, parser):
        '''
        Содержит описания аргументов командной строки для команды link_processing.
        '''
        parser.add_argument('link', type=str, help=u'Ссылка на логи')

    def handle(self, *args, **kwargs):
        '''
        Вызывает функию обработки лог-файла и записи его данных в БД

        :param kwargs: ссылка на лог файл
        '''
        link = kwargs['link']
        try:
            ufr = requests.get(link, stream=True)
            for line in ufr.iter_lines():
                self.log_parser(line.decode('UTF-8'))
        except:
            print("Stop.Error....")

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

    def log_parser(self, file_name):
        '''
        Функция записи данных из Apache лога в БД.
        :param file_name: имя файла, содержащего логи
        '''

        f = open(file_name, "r")
        lines = f.readlines()
        regex = '([(\w\.))]+) - (-|adva) \[(.*?)\] "(.*?)" (\d+) (\d+|-) "(.*?)" "(.*?)" "-"'

        '''
        #cпособ получения данных из лога без использования регулярных выражений (как вариат):
        for line in lines[1:]:

            elem = line.split(" ")
            #print (elem)
            ip_addr = elem[0]
            date = elem[3][1:]
            method = elem[5][1:]
            uri = elem[6]
            resp = elem[8]
            size = elem[9]
            #print(ip_addr, date, method, uri, resp, size )
        '''
        #начинаем с 1го элемента, так как нулевой - символ перевода строки
        for line in lines[1:]:
            if re.match(regex, line) is None:
                print("Log file does not match the format!!!!! Break....")
                break;
            data_line = re.match(regex, line).groups()
            #форматируем значение даты, чтобы не выводилось ничего лишнего, кроме ДД/ММ/ГГГГ
            #при этом дата выводится, как в логах
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
            print("saving done")
        f.close()

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
        f = open('LOG_FILE1', "wb")
        ufr = requests.get(link)  # делаем запрос
        f.write(ufr.content)  # записываем содержимое в файл
        f.close()
        self.log_parser('LOG_FILE1')

# -*- coding: utf-8 -*-

u"""
Модуль содержит тесты для функции парсинга логов по команде link_processing
"""
from django.test import TestCase
from LinkData.models import LinkData
import re

class TestLinkData (TestCase):
    u"""
    Тесты для модели LinkData и команды link_processing, пример вызова теста:

    python3 ./manage.py test LinkData.tests.TestLinkData.test_reg_exp -v3
    """
    def test_reg_exp(self):
        u"""
        Проверяет, что регулярное выражение из функции log_parser команды link_processing соотвествует
        формату строк лог-файла
        """
        regex = '([(\w\.))]+) - (-|adva) \[(.*?)\] "(.*?)" (\d+) (\d+|-) "(.*?)" "(.*?)" "-"'
        test_log = '1.2.3.5 - - [28/Dec/2020:19:33:08 +0100] "TEST /test/test/test" 200 4498 "http://test/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0" "-"'
        self.assertIsNotNone(re.match(regex, test_log))
        test_log = '1.2.3.5 - - [28/Dec/2020:19:33:08 +0100] "TEST /test/test/test" 200 4498 "http://test/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"'
        self.assertIsNone(re.match(regex, test_log))

    def test_add_to_db (self):
        u"""
        Проверяет, что данные корректно записываются в БД
        """
        test_log = '1.2.3.5 - - [28/Dec/2020:19:33:08 +0100] "TEST /test/test/test" 200 4498 "http://test/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0" "-"'
        regex = '([(\w\.))]+) - (-|adva) \[(.*?)\] "(.*?)" (\d+) (\d+|-) "(.*?)" "(.*?)" "-"'
        data_line = re.match(regex, test_log).groups()
        date = data_line[2].split(' ')[0]
        ind = date.index(':')
        date = str(date[:ind])
        new_el = LinkData(ip=data_line[0],
                          date=str(date),
                          http_method=data_line[3].split(' ')[0],
                          uri=data_line[3].split(' ')[1],
                          response_code=str(data_line[4]),
                          size=str(data_line[5]))
        self.assertTrue(LinkData.objects.filter(ip='1.2.3.5', http_method='TEST').exists())
        new_el.delete()
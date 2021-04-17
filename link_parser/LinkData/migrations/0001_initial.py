# Generated by Django 2.2.16 on 2021-04-15 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LinkData',
            fields=[
                ('id', models.AutoField(db_column='F_LOG_ID', primary_key=True, serialize=False)),
                ('ip', models.CharField(db_column='F_IP_ADDRESS', max_length=255, verbose_name='IP адрес')),
                ('date', models.DateField(blank=True, db_column='F_DATE', null=True, verbose_name='Дата')),
                ('http_method', models.CharField(db_column='F_HTTP_METHOD', max_length=255, verbose_name='HTTP метод')),
                ('uri', models.CharField(db_column='F_URI', max_length=255, verbose_name='URI запроса')),
                ('response_code', models.CharField(db_column='F_RESPONSE_CODE', max_length=255, verbose_name='Код ответа')),
                ('size', models.CharField(db_column='F_RESPONSE_SIZE', max_length=255, verbose_name='Размер ответа')),
            ],
        ),
    ]


#Класс для описания составляющих строк Apache лога


from django.db import models

class LinkData(models.Model):
    """Модель для описания распарсенных данных из лога.
     Поля модели содержат IP адрес, дату из лога, http метод (GET, POST,...),
    URI запроса, код ответов, размер ответа.
    URI может иметь большой размер, поэтмоу представлен, как TextField.
    """
    id = models.AutoField(auto_created=True, primary_key=True, unique=True, db_column="F_LOG_ID")
    ip = models.CharField(u"IP адрес", max_length=255, db_column="F_IP_ADDRESS")
    date = models.CharField(u"Дата", max_length=255, db_column="F_DATE", blank=True, null=True)
    http_method = models.CharField(u"HTTP метод", max_length=255, db_column="F_HTTP_METHOD")
    uri = models.TextField(u"URI запроса", db_column="F_URI", blank=True)
    response_code = models.CharField(u"Код ответа", max_length=255, db_column="F_RESPONSE_CODE")
    size = models.CharField(u"Размер ответа", max_length=255, db_column="F_RESPONSE_SIZE")

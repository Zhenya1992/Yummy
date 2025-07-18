from django.db import models


class Users(models.Model):
    """Класс для хранения информации о пользователях"""

    name = models.CharField(max_length=50)
    telegram = models.BigIntegerField(unique=True,)
    phone = models.CharField(max_length=15, null=True)



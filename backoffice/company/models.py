from django.db import models


# TODO: добавить таблицы Company, Opening

class Company(models.Model):
    name = models.CharField(max_length=100)
    inn = models.IntegerField(unique=True)

    class Meta:
        db_table = "company"
        ordering = ('id',)
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f'{self.name}'

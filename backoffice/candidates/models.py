from django.db import models
from system.models import Customer, Spec

# TODO: добавить таблицы CV, Education, Experience

class CV(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Кандидат')
    applicant_spec_id = models.ForeignKey(Spec, on_delete=models.CASCADE, verbose_name='Специальность')

    description = models.TextField(verbose_name="Описание")
    salary_min = models.IntegerField(verbose_name="Минимальная зарплата")
    salary_max = models.IntegerField(verbose_name="Максимальная зарплата")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

class Education(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Кандидат')

    university_name = models.CharField(max_length=100, verbose_name="Университет")
    faculty = models.CharField(max_length=100, verbose_name="Факультет")

    spec_id = models.ForeignKey(Spec, on_delete=models.CASCADE, verbose_name='Специальность')

    end_year = models.IntegerField(null=True, blank=True)

class Experience(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Кандидат')

    company = models.CharField(max_length=100, verbose_name="Предыдущее место работы")
    position = models.CharField(max_length=50, verbose_name="Должность")
    additional_info = models.TextField(verbose_name="Дополнительная информация", null=True, blank=True)

    start_date = models.DateField(verbose_name="Дата начала работы")
    end_date = models.DateField(verbose_name="Дата конца работы")


    
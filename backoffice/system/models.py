from django.db import models
from django.contrib.auth.models import User
from passlib.context import CryptContext

from company.models import Company

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class City(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "city"
        ordering = ('id',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
    
    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "grade"
        ordering = ('id',)
        verbose_name = 'Степень образования'
        verbose_name_plural = 'Степени образования'
    
    def __str__(self):
        return self.name


class Spec(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "spec"
        ordering = ('id',)
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
    
    def __str__(self):
        return self.name


class Customer(User):
    ROLES = [
        ('candidate', 'Соискатель'),
        ('hr', 'HR')
    ]

    GENDERS = [
        ('M', 'Мужской'),
        ('F', 'Женский')
    ]

    phone = models.CharField(max_length=32, verbose_name="Телефон", null=True, blank=True)
    telegram = models.CharField(max_length=32, verbose_name="Телеграм", null=True, blank=True)
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    gender = models.CharField(choices=GENDERS, default='M', verbose_name="Пол")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", related_name='city')
    job_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город поиска работы", null=True,
                                 blank=True, related_name='job_city')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="Уровень образования")

    def set_password_hash(self, password):
        self.password = pwd_context.hash(password)
        self.save()

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    class Meta:
        db_table = "customer"
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)


class HR:
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='HR')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        user = Customer.objects.filter(id=self.user_id)
        return f'{user.first_name} {user.last_name}'

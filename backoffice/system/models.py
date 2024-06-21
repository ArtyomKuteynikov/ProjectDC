from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Customer(User):
    ROLES = [
        ('candidate', 'Соискатель'),
        ('hr', 'HR')
    ]

    # TODO: добавить поля
    phone = models.CharField(max_length=32, verbose_name="Телефон")
    role = models.CharField(max_length=32, choises=ROLES)

    def set_password_hash(self):
        password = generate_password()
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


class City(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "city"
        ordering = ('id',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Grade(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "grade"
        ordering = ('id',)
        verbose_name = 'Степень образования'
        verbose_name_plural = 'Степени образования'


class Spec(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "spec"
        ordering = ('id',)
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


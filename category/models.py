from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Language(models.Model):
    language = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'{self.language}'


    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

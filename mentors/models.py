from django.db import models

from category.models import Language


# Create your models here.


class Mentor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    years_exp = models.IntegerField(default=1)
    language = models.ForeignKey(Language, on_delete=models.RESTRICT, related_name='mentors')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.language}'

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Ментора'
from django.db import models

from category.models import Category, Language
from mentors.models import Mentor
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    id = models.AutoField(primary_key=True)
    languages = models.ForeignKey(Language, on_delete=models.RESTRICT, related_name='languages')
    mentors = models.ForeignKey(Mentor, on_delete=models.RESTRICT, related_name='mentors')
    duration_months = models.IntegerField(default=3)
    cover = models.ImageField(upload_to='images/covers/', null=True, blank=True)
    favorite = models.ManyToManyField(User, related_name='favorites', blank=True)

    def __str__(self):
        return f'{self.title}  - {self.category}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class CourseImages(models.Model):
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='images/course_images/')
    course = models.ForeignKey(Course, related_name='images', on_delete=models.CASCADE)

    def generate_name(self):
        from random import randint
        return 'image' + str(self.title) + str(randint(100000, 1_000_000))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(CourseImages, self).save(*args, **kwargs)

    def __str__(self):
        return '{} || {}'.format(self.title, self.course)

    class Meta:
        verbose_name_plural = 'Course Images'

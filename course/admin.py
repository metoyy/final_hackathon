from django.contrib import admin

from course.models import Course, CourseImages, Purchase

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseImages)
admin.site.register(Purchase)
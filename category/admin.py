from django.contrib import admin

from category.models import Category, Language

# Register your models here.
admin.site.register(Category)
admin.site.register(Language)
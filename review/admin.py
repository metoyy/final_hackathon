from django.contrib import admin

from review.models import Review

# Register your models here.
@admin.register(Review)
class Rev(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at', 'rating_score')
    list_filter = ('rating_score',)
    search_fields = ('user', 'course')
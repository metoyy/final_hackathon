from django.contrib import admin

from course.models import Course, CourseImages, Purchase
from review.models import Review

# Register your models here.
admin.site.register(CourseImages)
admin.site.register(Purchase)

@admin.register(Course)
class Courses(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'bought', 'reviews_count', 'category', 'language', 'mentors', 'months',)
    list_filter = ('mentors',)
    search_fields = ('title__istartswith', 'category__istartswith', 'language__istartswith', 
                     'mentors__istartswith')

    def months(self, obj):
        course = Course.objects.get(id=obj.id)
        return course.duration_months
    
    def bought(self, obj):
        course = Course.objects.get(id=obj.id)
        count = Purchase.objects.filter(course=course).count()
        return count

    def reviews_count(self, obj):
        course = Course.objects.get(id=obj.id)
        reviews = Review.objects.filter(course=course).count()
        return reviews

    reviews_count.short_description = 'Reviews'

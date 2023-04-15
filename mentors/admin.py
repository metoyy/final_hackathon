from django.contrib import admin

from mentors.models import Mentor
from course.models import Course

# Register your models here.
@admin.register(Mentor)
class Mentar(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'years_exp', 'language', 'courses_count')
    list_filter = ('language',)
    search_fields = ('first_name', 'last_name', 'language')

    def courses_count(self, obj):
        mentor = Mentor.objects.get(id=obj.id)
        courses = Course.objects.filter(mentors=mentor).count()
        return courses
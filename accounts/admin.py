from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import CustomUser
User = get_user_model()

# Register your models here.
@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'show_count_courses', 'likes', 
                    'favs', 'last_login', 'date_joined', 'is_active', 'is_superuser', 'is_staff')
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    search_fields = ('username__istartswith', 'first_name__istartswith', 'last_name__istartswith', 'email__istartswith')

    def show_count_courses(self, obj):
        user = User.objects.get(id=obj.id)
        result = user.purchased_courses.count()
        return result

    def likes(self, obj):
        result = User.objects.get(id=obj.id).likes.count()
        return result
    
    def favs(self, obj):
        user = User.objects.get(id=obj.id)
        result = user.favorites.count()
        return result

    likes.short_description = 'LIKES'
    show_count_courses.short_description = 'Courses Purchased'
    

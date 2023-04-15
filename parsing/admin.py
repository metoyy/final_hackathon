from django.contrib import admin

from parsing.models import Call

@admin.register(Call)
class Gop(admin.ModelAdmin):
    list_display = ('number', 'question', 'date_added', 'telegram_user')
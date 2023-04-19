from django.db import models
from django.utils.timezone import now


class Call(models.Model):
    number = models.CharField(max_length=250)
    question = models.TextField(default='I need call')
    date_added = models.DateTimeField(default=now, editable=False)
    telegram_user = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}  ||  {}'.format(self.number, self.question)

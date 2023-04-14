from django.db import models


class Call(models.Model):
    number = models.CharField(max_length=250)
    question = models.TextField(default='I need call')

    def __str__(self):
        return '{}  ||  {}'.format(self.number, self.question)

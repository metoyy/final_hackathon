from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course

User = get_user_model()



class Like(models.Model):
    owner = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'course']

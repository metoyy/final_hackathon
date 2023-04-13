from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course

User = get_user_model()



class Review(models.Model):
    RATING_CHOICES = (
        (1, 'Too Bad'), (2, 'Bad'), (3, 'Okay'), (4, 'Good'), (5, 'Perfect')
    )

    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    rating_score = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']
    def __str__(self):
        return f'User {self.user}\'s review on {self.course.title}'
from rest_framework import serializers

from category.models import Category
from course.serializers import CoursesListSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['courses count'] = instance.courses.count()
        repr['courses'] = CoursesListSerializer(instance=instance.objects.all(), many=True).data



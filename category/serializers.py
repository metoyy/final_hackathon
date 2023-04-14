from rest_framework import serializers

from category.models import Category, Language
from course.serializers import CoursesListSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['courses count'] = instance.courses.count()
        repr['courses'] = CoursesListSerializer(instance=instance.courses.all(), many=True, context=self.context).data
        return repr


class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

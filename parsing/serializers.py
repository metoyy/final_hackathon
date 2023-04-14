from rest_framework import serializers

from course.models import Course
from parsing.models import Call


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'


class CoursesParsingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent.pop('category')
        represent.pop('language')
        represent['category'] = instance.category.name
        represent['language'] = instance.language.language
        return represent

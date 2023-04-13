from django.db.models import Avg
from rest_framework import serializers

from category.models import Category
from course.models import Course, CourseImages


class CourseImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImages
        fields = '__all__'

class CoursesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'category', 'duration_months')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['reviews count'] = instance.reviews.count()
        repr['average rating for this product'] = instance.reviews.aggregate(Avg('rating_score'))['rating_score__avg']
        return repr


class CourseCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(required=True, queryset=Course.objects.all())
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    book_cover = CourseImagesSerializer(many=True, required=False)
    class Meta:
        model = Course
        fields = ('title', 'mentors', 'category', 'cover', 'price', 'languages', 'duration_months')

    def create(self, validated_data):
        request = self.context.get('request')
        course = Course.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            CourseImages.objects.create(images=image, course=course)
        return


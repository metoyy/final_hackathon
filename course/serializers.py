from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser

from category.models import Category
from course.models import Course, CourseImages


class CourseImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImages
        fields = '__all__'


class CoursesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'category', 'duration_months')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes_count'] = instance.likes.count()
        repr['reviews_count'] = instance.reviews.count()
        repr['average_rating for this product'] = instance.reviews.aggregate(Avg('rating_score'))['rating_score__avg']
        request = self.context['request']
        user = request.user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance, user)
            repr['is_favorite'] = self.is_favorite(instance, user)
        return repr

    @staticmethod
    def is_favorite(course, user):
        return user.favorites.filter(id=course.id).exists()
    
    @staticmethod
    def is_liked(course, user):
        return user.likes.filter(course=course).exists()


class CourseCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())

    class Meta:
        model = Course
        fields = ('title', 'mentors', 'category', 'cover',
                  'price', 'duration_months')

    def create(self, validated_data):
        request = self.context.get('request')
        course = Course.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            CourseImages.objects.create(images=image, course=course)
        return


from django.db.models import Avg, Count, Max
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
        repr['reviews count'] = instance.reviews.count()
        repr['likes_count'] = instance.likes.count()
        repr['reviews_count'] = instance.reviews.count()
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
    course = serializers.PrimaryKeyRelatedField(required=True, queryset=Course.objects.all())
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    book_cover = CourseImagesSerializer(many=True, required=False)

    class Meta:
        model = Course
        fields = ('course', 'title', 'mentors', 'category', 'cover', 'price', 'languages', 'duration_months', 'book_cover')

    def create(self, validated_data):
        request = self.context.get('request')
        course = Course.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            CourseImages.objects.create(images=image, course=course)
        return



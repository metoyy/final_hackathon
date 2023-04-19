from rest_framework import serializers

from review.models import Review
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    course_id = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ('id', 'first_name', 'last_name', 'rating_score', 'body', 'course_id', 'created_at')


class ReviewDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = ('id', 'first_name', 'last_name', 'user', 'rating_score', 'body', 'created_at', 'user_email')


class MyReviewsSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    course_id = serializers.ReadOnlyField(source='course.id')
    course_name = serializers.ReadOnlyField(source='course.title')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ('id', 'first_name', 'last_name', 'rating_score', 'body',
                  'created_at', 'course_id', 'course_name')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        user = User.objects.get(id=instance.user.id)
        represent = super().to_representation(instance)
        represent['user'] = UserSerializer(user)
        return represent
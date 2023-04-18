from rest_framework import serializers

from review.models import Review


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

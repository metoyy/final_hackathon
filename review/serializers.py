from rest_framework import serializers

from review.models import Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    course_id = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ('username', 'rating_score', 'body', 'created_at', 'course_id')

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review


class ReviewDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = ('user', 'rating_score', 'body', 'created_at')


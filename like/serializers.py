from rest_framework import serializers
from django.contrib.auth import get_user_model

from like.models import Like

User = get_user_model()

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_name = serializers.ReadOnlyField(source='owner.first_name')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        course = attrs['course']
        if user.likes.filter(course=course).exists():
            raise serializers.ValidationError('You already liked this course!')
        return attrs


class LikeListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_name = serializers.ReadOnlyField(source='owner.first_name')

    class Meta:
        model = Like
        fields = ('owner', 'owner_name',)



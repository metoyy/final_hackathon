from rest_framework import serializers

from mentors.models import Mentor


class MentorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


class MentorCreateSerializer(serializers.ModelSerializer):
    years_exp = serializers.IntegerField(required=True)

    class Meta:
        model = Mentor
        fields = '__all__'

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from category.models import Category, Language
from course.models import Course, CourseImages, Purchase


User = get_user_model()

class CourseImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImages
        fields = '__all__'


class CoursesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'category', 'duration_months', 'language')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
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
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    language = serializers.PrimaryKeyRelatedField(required=True, queryset=Language.objects.all())

    class Meta:
        model = Course
        fields = ('title', 'mentors', 'category', 'cover',
                  'price', 'duration_months', 'description', 'language')

    def create(self, validated_data):
        request = self.context.get('request')
        course = Course.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            CourseImages.objects.create(images=image, course=course)
        return course



class PurchaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Purchase
        fields = "__all__"


class ConfirmPurchaseSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True, max_length=255)
    default_error_messages = {
        'bad_code': _('Code is expired or invalid!')
    }

    def validate(self, attrs):
        self.confirmation_code = attrs['confirmation_code']
        return super().validate(attrs)


    def save(self, **kwargs):
        try:
            user = User.objects.get(activation_code=self.confirmation_code)
            user.activation_code = ''
            user.save()
        except User.DoesNotExist:
            self.fail('bad_code')



class CoursesDetailSerializer(CoursesListSerializer):
    class Meta:
        model = Course
        exclude = "favorite",

    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     repr['description'] = instance.description
    #     repr['price'] = instance.price
    #     return repr
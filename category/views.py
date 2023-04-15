from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import Category, Language
from course.serializers import CoursesListSerializer
from . import serializers


#
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = permissions.AllowAny,

    def get_permission(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryDetailsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),

    @action(['GET'], detail=True)
    def courses(self, request, pk):
        self.request = request
        category = self.get_object()
        courses = category.courses.all()
        serializer = CoursesListSerializer(instance=courses, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    @action(['DELETE'], detail=True)
    def perform_destroy(self, instance):
        category = instance.category
        instance.delete()
        category.delete()
        return Response('Deleted!', status=201)


class LanguageListView(APIView):
    permission_classes = permissions.AllowAny,

    @swagger_auto_schema
    def get(self, request):
        queryset = Language.objects.all()
        serializer = serializers.LanguageListSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=200)

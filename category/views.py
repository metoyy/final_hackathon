from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from category.models import Category
from course.serializers import CoursesListSerializer
from . import serializers


#
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permission(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),

# Create your views here.
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryDetailsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser()

    @action(['GET'], detail=True)
    def courses(self, request, pk):
        category = self.get_object()
        courses = category.courses.all()
        serializer = CoursesListSerializer(instance=courses, many=True)
        return Response(serializer.data, status=200)

    @action(['DELETE'], detail=True)
    def perform_destroy(self, instance):
        category = instance.category
        instance.delete()
        category.delete()
        return Response('Deleted!', status=201)

from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from category.models import Category
from course.serializers import CoursesListSerializer
from . import serializers

# Create your views here.
class CategoryRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser()

    @action(['GET'], detail=True)
    def get(self):
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

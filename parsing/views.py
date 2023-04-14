from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

from course import serializers
from course.models import Course


class AllCoursesView(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CoursesParsingSerializer(instance=courses, many=True)
        return Response(serializer.data, status=200)


class LeaveNumberView(APIView):
    permission_classes = permissions.AllowAny,

    def post(self, request):
        data = request.data
        serializer = CallSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'success'}, status=200)

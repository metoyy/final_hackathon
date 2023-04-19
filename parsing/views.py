from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import get_user_model

from course import serializers
from course.models import Course
from .tasks import send_call_to_admins
from accounts.serializers import *

User = get_user_model()


class AllCoursesView(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CoursesParsingSerializer(instance=courses, many=True)
        return Response(serializer.data, status=200)


class LeaveNumberView(APIView):
    permission_classes = permissions.AllowAny,

    def post(self, request):
        qs = User.objects.filter(is_superuser=True)
        try:
            admin_users = [x.email for x in qs]
        except Exception as e:
            print(e)
        data = request.data
        serializer = CallSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True)
        send_call_to_admins.delay(users=admin_users, number=data['number'],
                            text=data['question'], tg_user=data['telegram_user'])
        
        return Response({'msg': 'success'}, status=200)


class AllAccountsView(APIView):
    permission_classes = permissions.AllowAny,

    def get(self, request):
        qs = User.objects.all()
        serializer = UserSerializer(instance=qs, many=True)
        return Response(serializer.data, status=200)

import uuid

from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError

from course import serializers
from course.models import Course
from .tasks import send_call_to_admins
from accounts.serializers import *
from .tasks import send_conf_email_telegram

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


class AddAccountView(APIView):
    permission_classes = permissions.AllowAny,

    def patch(self, request):

        user = User.objects.filter(email=request.data['email'])
        if user.exists() and user.first().telegram_username in (None, '', False):
            user = user.first()
            user.tg_code = uuid.uuid4()
            user.save()
            send_conf_email_telegram.delay(user.email, user.tg_code)
            return Response({'msg': 'Confirmation email with code sent.'}, status=200)
        else:
            return Response({'msg': 'User not found or linked to another account!'}, status=404)

    def post(self, request):
        user1 = User.objects.filter(telegram_username=request.data['username'])
        if user1.exists():
            return Response({'msg': f'You already linked with user: {user1.first().email}'}, status=400)
        try:
            requested_user = User.objects.get(tg_code=request.data['code'])
        except (User.DoesNotExist,
                KeyError,
                MultiValueDictKeyError):
            return Response({'msg': 'User not found, or invalid code!'}, status=404)
        requested_user.telegram_username = request.data['username']
        requested_user.tg_code = None
        requested_user.save()
        return Response({'msg': 'Success'}, status=201)

    def delete(self, request):
        try:
            user = User.objects.get(telegram_username=request.data['username'])
        except User.DoesNotExist:
            return Response({'msg': 'You were not linked to an account!'}, status=400)
        user.telegram_username = None
        user.tg_code = None
        user.save()
        return Response({'msg': 'Success'}, status=204)


class AccountDetails(APIView):
    permission_classes = permissions.AllowAny,

    def get(self, request, pk):
        user = User.objects.get(telegram_username=pk)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        user = User.objects.get(telegram_username=pk)
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success'}, status=201)


class CheckView(APIView):
    permission_classes = permissions.AllowAny,

    def get(self, request):
        try:
            request.data['username']
        except KeyError:
            return Response({'msg': 'Key error! "username"'}, status=401)
        try:
            user = User.objects.get(telegram_username=request.data['username'])
        except User.DoesNotExist:
            return Response({'msg': 'User was not found!'}, status=400)
        return Response({'msg': 'All OK!'}, status=200)


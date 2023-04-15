from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from mentors import serializers
from mentors.models import Mentor


class MentorsListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),

    def get(self, request):
        mentors = Mentor.objects.all()
        serializer = serializers.MentorListSerializer(instance=mentors, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(request_body=serializers.MentorCreateSerializer)
    def post(self, request):
        data = request.data
        serializer = serializers.MentorCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

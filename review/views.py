from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView

from course.models import Course
from . import serializers
from .models import Review
from .permissions import IsUserOrAdmin


class ReviewCreateView(APIView):

    @swagger_auto_schema(request_body=serializers.ReviewCreateSerializer)
    def post(self, request):
        user = request.user
        try:
            course = Course.objects.get(id=request.data['course_id'])
        except Course.DoesNotExist:
            return Response({'msg': 'Course not found!'}, status=404)
        review = course.reviews.filter(user=user)
        if review.exists():
            serializer = serializers.ReviewCreateSerializer(instance=review, many=True).data
            return Response({'msg': 'You already left the review!', 'review': serializer}, status=400)
        serializer = serializers.ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=200)


class ReviewDetailView(generics.RetrieveDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewDetailSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return IsUserOrAdmin(),
        return permissions.AllowAny(),


class CourseReviewListView(APIView):
    permission_classes = permissions.AllowAny,

    @staticmethod
    def get(request, pk):
        course = Course.objects.get(id=pk)
        serializer = serializers.ReviewDetailSerializer(instance=course.reviews, many=True).data
        return Response(serializer, status=200)


class MyReviewsView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request):
        user = request.user
        reviews = Review.objects.filter(user=user)
        serializer = serializers.MyReviewsSerializer(instance=reviews, many=True).data
        return Response(serializer, status=200)


class ReviewListView(APIView):
    def get(self, request):
        qs = Review.objects.all()
        serializer = serializers.ReviewSerializer(instance=qs, many=True)
        return Response(serializer.data, status=200)

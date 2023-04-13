from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from like import serializers
from like.models import Like
from course.models import Course
from like.permissions import IsAuthor


class LikeCreateDeleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({'msg': 'Post not found!'}, status=404)
        if not course.likes.filter(owner=request.user).exists():
            data = request.data.copy()
            data['course'] = course.id
            serializer = serializers.LikeSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            return Response({'msg': 'success'}, status=200)
        else:
            user_like = Like.objects.get(owner=request.user)
            user_like.delete()
            return Response({'msg': 'like deleted!'}, status=204)
        
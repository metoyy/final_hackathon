from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView

from . import serializers
from .models import Review
from .permissions import IsUserOrAdmin


class ReviewCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ReviewCreateSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ReviewDetailView(generics.RetrieveDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewDetailSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return IsUserOrAdmin(),
        return permissions.IsAuthenticated(),



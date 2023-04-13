from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from course import serializers


from course.models import Course


class StandardResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class CoursesViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = StandardResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('price', 'category', 'languages',)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CourseCreateSerializer
        return serializers.CoursesListSerializer



    def get_permissions(self):
        if self.action in ('destroy', 'create', 'update', 'partial_update'):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]








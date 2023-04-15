from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from course import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


from course.models import Course


class StandardResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class CoursesViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = StandardResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('price', 'category', 'language',)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CourseCreateSerializer
        return serializers.CoursesListSerializer

    def get_permissions(self):
        if self.action in ('destroy', 'create', 'update', 'partial_update'):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class FavoriteAddOrDeletePost(APIView):
    def post(self, request, pk):
        course = Course.objects.get(id=pk)
        if course.favorite.filter(id=request.user.id).exists():
            course.favorite.remove(request.user)
        else:
            course.favorite.add(request.user)
        return Response({'msg': 'Successfully added post to favorites'}) \
        if course.favorite.exists() else \
Response({'msg': 'Successfully deleted post of favorites'})



class FeaturedCoursesView(APIView):
    permission_classes = permissions.IsAuthenticated,


    def get(self, request):
        from collections import Counter
        user = request.user
        courses = user.favorites.all()
        langs = [x.language for x in courses]
        featured_lg = Counter(langs).most_common(1)[0][0]
        featured_courses = Course.objects.filter(language=featured_lg)
        serializer = serializers.CoursesListSerializer(instance=featured_courses, many=True,
                                                       context={'request': request})
        return Response(serializer.data, status=200)

class FavoriteCourseListView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request):
        user = request.user
        courses = user.favorites.all()
        serializer = serializers.CoursesListSerializer(instance=courses, many=True,
                                                       context={'request': request})
        return Response(serializer.data, status=200)



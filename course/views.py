import uuid
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.contrib.auth import get_user_model

from accounts.tasks import confirm_purchase_mail
from course import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


from course.models import Course, Purchase

User = get_user_model()


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
        elif self.action == 'retrieve':
            return serializers.CoursesDetailSerializer
        return serializers.CoursesListSerializer

    def get_permissions(self):
        if self.action in ('destroy', 'create', 'update', 'partial_update'):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class FavoriteAddOrDeletePost(APIView):
    permission_classes = permissions.IsAuthenticated,

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




class PurchaseCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        course = Course.objects.get(id=pk)
        user = request.user
        if not course.purchased_courses.filter(owner=user).exists():
            if user.activation_code is not None and user.activation_code != '':
                return Response({'msg': '\nThank You for your support!\nPlease confirm your purchase by entering '
                                        'the code'
                                        'we sent to your mail!'},
                                status=200)
            user.activation_code = uuid.uuid4()
            user.save()
            confirm_purchase_mail.delay(user.email, user.activation_code)
            return Response({'msg': 'Confirmation code sent!'}, status=200)
        else:
            return Response({"msg": "You\'ve already bought this course!"}, status=400)


    @staticmethod
    @swagger_auto_schema(request_body=serializers.ConfirmPurchaseSerializer)
    def put(request, pk):
        try:
            serializer = serializers.ConfirmPurchaseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as err:
            print(err)
            return Response({'msg': 'Code expired or invalid!'}, status=400)
        else:
            course = Course.objects.get(id=pk)
            data = request.data.copy()
            data['course'] = course.id
            serializer = serializers.PurchaseSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            return Response({'msg': 'Successfully purchased!'}, status=200)


class PurchaseListView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request):
        user = request.user
        courses = Course.objects.filter(Q(purchased_courses__owner=user))
        serializer = serializers.CoursesDetailSerializer(instance=courses, many=True,
                                                       context={'request': request})
        return Response(serializer.data, status=200)

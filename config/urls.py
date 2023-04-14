from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from category.views import LanguageListView


schema_view = get_schema_view(
   openapi.Info(
      title="HACKATHON DOCS",
      default_version='v1',
      description="API DOCS for hackathon project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="abass@ali.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('all-auth/', include('allauth.urls')),

    path('api/categories/', include('category.urls')),
    path('api/courses/', include('course.urls')),
    path('api/reviews/', include('review.urls')),
    path('api/languages/', include('lang.urls')),
    path('api/mentors/', include('mentors.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

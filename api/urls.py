from django.urls import path, include
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

from api.views import (
    StudentsViewSet,
    CourseViewSet,
    LessonListCreateView,
    LessonRetrieveUpdateDestroyView,
    PaymentListAPIView,
)

router = routers.DefaultRouter()
router.register("students", StudentsViewSet)
router.register("courses", CourseViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateView.as_view()),
    path("lessons/<int:pk>/", LessonRetrieveUpdateDestroyView.as_view()),
    path("payment/all/", PaymentListAPIView.as_view(), name="payments"),
    path('docs/', include_docs_urls(title='API documentation')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

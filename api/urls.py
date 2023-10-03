from django.urls import path, include
from rest_framework import routers

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

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateView.as_view()),
    path("lessons/<int:pk>/", LessonRetrieveUpdateDestroyView.as_view()),
    path("payment/all/", PaymentListAPIView.as_view(), name="payments"),
]

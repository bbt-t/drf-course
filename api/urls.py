from django.urls import path, include
from rest_framework import routers

from api.views import StudentsViewSet, CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView

router = routers.DefaultRouter()
router.register('students', StudentsViewSet)
router.register('courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view()),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view()),
]

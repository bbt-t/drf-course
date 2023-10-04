from rest_framework import serializers

from api.models import Course, Lesson, Payment
from auth_api.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["email", "city", "phone"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

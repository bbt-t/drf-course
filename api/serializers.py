from rest_framework import serializers

from api.models import Student, Course, Lesson


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'city', 'phone']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'description']

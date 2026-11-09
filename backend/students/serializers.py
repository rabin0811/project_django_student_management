from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    course_display = serializers.CharField(source='get_course_display', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'age', 'course', 'course_display', 'enrollment_date']

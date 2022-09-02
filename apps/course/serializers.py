from rest_framework import serializers
from .models import CourseCategory, Course


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = [
            'id', 'title'
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id', 'title', 'subtitle',
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'teacher', 'title', 'subtitle', 'image', 'video', 'description', 'duration_month',
        )

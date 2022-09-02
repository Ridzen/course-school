from django.urls import re_path, include

from .views import CourseCategoryListAPIView, CourseDetailAPIView, CourseListCreateAPIView

urlpatterns = [
    re_path('course-category/', CourseCategoryListAPIView.as_view(), name='course-category'),
    re_path('course-detail/', CourseDetailAPIView.as_view(), name='course-detail'),
    re_path('course=list/', CourseDetailAPIView.as_view(), name='course-list'),
]
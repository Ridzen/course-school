from django.contrib import admin
from .models import CourseCategory, Course
# Register your models here.


@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    pass


@admin.register(CourseCategory)
class AdminCourseCategory(admin.ModelAdmin):
    pass

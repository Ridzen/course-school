from django.contrib import admin
from apps.mentors.models import CustomUser


@admin.register(CustomUser)
class TeacherAdmin(admin.ModelAdmin):
    pass
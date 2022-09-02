from django.contrib import admin
from .models import Category, MasterClass

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(MasterClass)
class MasterClassAdmin(admin.ModelAdmin):
    pass
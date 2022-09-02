from rest_framework import serializers
from .models import MasterClass, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class MasterClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterClass
        fields = [
            'id', 'title', 'category', 'subtitle', 'description', 'start_date', 'amount_lessons', 'image',
              'overview', 'duration', 'created_at', 'in_archive'
        ]


class MasterClassListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterClass
        fields = [
            'id', 'title', 'category', 'subtitle', 'description', 'start_date', 'amount_lessons', 'image',
              'overview', 'duration', 'created_at', 'in_archive'
        ]



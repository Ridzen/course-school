from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.course.models import CourseCategory, Course
from apps.course.serializers import CourseCategorySerializer, CourseSerializer, CourseDetailSerializer


# Create your views here.


class CourseCategoryListAPIView(generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class CourseDetailAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all
    serializer_class = CourseSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    search_fields = ["name", "role"]
    queryset = Course.objects.all()

    def post(self, request):
        request_body = request.data
        srz = CourseSerializer(data=request_body)
        if srz.is_valid():
            srz.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST, )

    @classmethod
    def get_extra_actions(cls):
        return []


class HeroRetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            product = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        srz = CourseSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return JsonResponse({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

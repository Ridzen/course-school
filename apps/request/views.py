from django.http import JsonResponse, HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page

from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.request.models import Questionnaire
from apps.request.serializers import QuestionnaireSerializer


class QuestionnaireAPIView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['name', 'surname']
    serializer_class = QuestionnaireSerializer
    # search_fields = ['surname']
    ordering_fields = ['created_at']
    queryset = Questionnaire.objects.all()


class QuestionnaireRetrieveAPIView(APIView):
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get(self, request, pk):
        try:
            product = Questionnaire.objects.get(id=pk)
        except Questionnaire.DoesNotExist:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        srz = QuestionnaireSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = Questionnaire.objects.get(id=pk)
        except Questionnaire.DoesNotExist:
            return JsonResponse({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

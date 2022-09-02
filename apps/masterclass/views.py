from rest_framework import generics

from django_filters import rest_framework as filters

from .models import MasterClass
from .serializers import MasterClassSerializer, MasterClassListSerializer

# Create your views here.


class MasterClassListView(generics.ListAPIView):
    queryset = MasterClass.objects.all()
    serializer_class = MasterClassListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('title',)


class MasterClassDetailView(generics.RetrieveAPIView):
    queryset = MasterClass.objects.all()
    serializer_class = MasterClassSerializer

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CategorySerializer, SubcategorySerializer, EventSerializer, SponsorSerializer
from .models import Category, Subcategory, Event, Sponsor


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', )

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', 'category')

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', 'subcategory')

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    http_method_names = ['get']
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *


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

class Our_SponsorViewSet(viewsets.ModelViewSet):
    queryset = Our_Sponsor.objects.all()
    serializer_class = Our_SponsorSerializer
    http_method_names = ['get']

class Prev_SponsorViewSet(viewsets.ModelViewSet):
    queryset = Prev_Sponsor.objects.all()
    serializer_class = Prev_SponsorSerializer
    http_method_names = ['get']

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.order_by('id').reverse()
    serializer_class = NotificationSerializer
    http_method_names = ['get']

from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class Our_SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Our_Sponsor
        fields = '__all__'

class Prev_SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prev_Sponsor
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

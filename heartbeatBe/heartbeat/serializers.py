from asyncio import TaskGroup

from rest_framework import serializers,routers,viewsets
from .models import UrlItem

class UrlItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UrlItem
        fields = ['id', 'url', 'status', 'created_at']
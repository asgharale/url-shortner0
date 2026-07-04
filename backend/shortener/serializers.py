from django.conf import settings
from rest_framework import serializers

from .models import Link


class LinkCreateSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2048)


class LinkResponseSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["original_url", "short_code", "short_url", "clicks", "created_at"]

    def get_short_url(self, obj):
        return f"{settings.SITE_BASE_URL}/{obj.short_code}"
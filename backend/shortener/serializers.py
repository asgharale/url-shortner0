from django.conf import settings
from rest_framework import serializers
from .models import Link, ProLink, WheelRedirect


class LinkCreateSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2048)
    domain = serializers.CharField(required=False, allow_blank=True)


def _build_short_url(obj, context):
    domain = context.get("domain")
    if domain:
        return f"https://{domain}/{obj.short_code}"
    request = context.get("request")
    if request is not None:
        return request.build_absolute_uri(f"/{obj.short_code}")
    return f"{settings.SITE_BASE_URL}/{obj.short_code}"


class LinkResponseSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["original_url", "short_code", "short_url", "clicks", "created_at"]

    def get_short_url(self, obj):
        return _build_short_url(obj, self.context)


class ProLinkResponseSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ProLink
        fields = ["original_url", "short_code", "short_url", "clicks", "created_at"]

    def get_short_url(self, obj):
        return _build_short_url(obj, self.context)
    


class WheelRedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WheelRedirect
        fields = ["url", "created_at"]
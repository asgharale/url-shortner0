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
        request = self.context.get("request")
        if request is not None:
            # Uses whichever domain the request actually came in on
            # (respects X-Forwarded-Proto from nginx for https)
            return request.build_absolute_uri(f"/{obj.short_code}")
        # Fallback if there's no request in context (e.g. shell/management command)
        from django.conf import settings
        return f"{settings.SITE_BASE_URL}/{obj.short_code}"
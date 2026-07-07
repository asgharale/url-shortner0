from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Link
from .serializers import LinkCreateSerializer, LinkResponseSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def shorten_url(request):
    serializer = LinkCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    original_url = serializer.validated_data["url"]
    chosen_domain = serializer.validated_data.get("domain", "").strip()

    from django.conf import settings
    if chosen_domain and chosen_domain not in settings.ALLOWED_SHORT_DOMAINS:
        return Response(
            {"domain": [f"'{chosen_domain}' is not an allowed domain."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    link, _created = Link.objects.get_or_create(original_url=original_url)

    return Response(
        LinkResponseSerializer(
            link, context={"request": request, "domain": chosen_domain or None}
        ).data,
        status=status.HTTP_201_CREATED,
    )


def redirect_short_code(request, short_code):
    link = get_object_or_404(Link, short_code=short_code)
    destination = link.original_url
    Link.objects.filter(pk=link.pk).update(clicks=F("clicks") + 1)
    return redirect(destination)
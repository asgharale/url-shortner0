from django.conf import settings
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Link, ProLink, WheelRedirect
from .serializers import LinkCreateSerializer, LinkResponseSerializer, ProLinkResponseSerializer, WheelRedirectSerializer


def _validate_domain(chosen_domain):
    if chosen_domain and chosen_domain not in settings.ALLOWED_SHORT_DOMAINS:
        return Response(
            {"domain": [f"'{chosen_domain}' is not an allowed domain."]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def shorten_url(request):
    serializer = LinkCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    original_url = serializer.validated_data["url"]
    chosen_domain = serializer.validated_data.get("domain", "").strip()

    err = _validate_domain(chosen_domain)
    if err:
        return err

    link, _created = Link.objects.get_or_create(original_url=original_url)
    return Response(
        LinkResponseSerializer(link, context={"request": request, "domain": chosen_domain or None}).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def shorten_pro_url(request):
    serializer = LinkCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    original_url = serializer.validated_data["url"]
    chosen_domain = serializer.validated_data.get("domain", "").strip()

    err = _validate_domain(chosen_domain)
    if err:
        return err

    link, _created = ProLink.objects.get_or_create(original_url=original_url)
    return Response(
        ProLinkResponseSerializer(link, context={"request": request, "domain": chosen_domain or None}).data,
        status=status.HTTP_201_CREATED,
    )


def redirect_short_code(request, short_code):
    link = Link.objects.filter(short_code=short_code).first()
    if link is not None:
        Link.objects.filter(pk=link.pk).update(clicks=F("clicks") + 1)
        return redirect(link.destination_url)

    pro_link = get_object_or_404(ProLink, short_code=short_code)
    ProLink.objects.filter(pk=pro_link.pk).update(clicks=F("clicks") + 1)
    return redirect(pro_link.destination_url)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def latest_wheel_redirect(request):
    latest = WheelRedirect.objects.first()  # Meta.ordering = "-created_at", so first() = newest
    if latest is None:
        return Response({"detail": "No redirect URL configured yet."}, status=status.HTTP_404_NOT_FOUND)
    return Response(WheelRedirectSerializer(latest).data)
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

    link, _created = Link.objects.get_or_create(original_url=original_url)

    return Response(
        LinkResponseSerializer(link, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


def redirect_short_code(request, short_code):
    link = get_object_or_404(Link, short_code=short_code)
    link.clicks += 1
    link.save(update_fields=["clicks"])
    return redirect(link.original_url)
from django import forms
from django.contrib import admin, messages
from django.shortcuts import render

from .models import Link


class BulkUrlForm(forms.Form):
    new_url = forms.URLField(label="New destination URL", max_length=2048)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("short_code", "original_url", "clicks", "created_at")
    search_fields = ("short_code", "original_url")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    actions = ["bulk_update_url"]

    @admin.action(description="Update original URL for selected links")
    def bulk_update_url(self, request, queryset):
        if request.POST.get("apply") == "yes":
            form = BulkUrlForm(request.POST)
            if form.is_valid():
                new_url = form.cleaned_data["new_url"]
                updated = queryset.update(original_url=new_url)
                self.message_user(
                    request, f"Updated the destination URL for {updated} link(s).", messages.SUCCESS
                )
                return None
        return render(
            request,
            "admin/shortener/link/bulk_update_url.html",
            context={"links": queryset, "opts": self.model._meta, "title": "Bulk update destination URL"},
        )
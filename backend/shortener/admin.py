from django import forms
from django.contrib import admin, messages
from django.shortcuts import render

from .models import Link


class BulkUrlForm(forms.Form):
    new_url = forms.URLField(
        label="Override URL (leave empty to clear the override)",
        max_length=2048,
        required=False,
    )


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("short_code", "original_url", "my_url", "effective_destination", "clicks", "created_at")
    search_fields = ("short_code", "original_url", "my_url")
    list_filter = ("created_at",)
    ordering = ("-clicks",)
    actions = ["bulk_update_url"]

    @admin.display(description="Redirects to")
    def effective_destination(self, obj):
        return obj.destination_url

    @admin.action(description="Set override URL (my_url) for selected links")
    def bulk_update_url(self, request, queryset):
        if request.POST.get("apply") == "yes":
            form = BulkUrlForm(request.POST)
            if form.is_valid():
                new_url = form.cleaned_data["new_url"]  # "" if left blank
                updated = queryset.update(my_url=new_url)
                if new_url:
                    msg = f"Set override URL for {updated} link(s)."
                else:
                    msg = f"Cleared override for {updated} link(s) — they'll redirect to original_url again."
                self.message_user(request, msg, messages.SUCCESS)
                return None
        return render(
            request,
            "admin/shortener/link/bulk_update_url.html",
            context={"links": queryset, "opts": self.model._meta, "title": "Bulk set override URL"},
        )
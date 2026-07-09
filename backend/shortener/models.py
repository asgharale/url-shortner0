import secrets
import string

from django.db import models

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7


def generate_short_code() -> str:
    """Unique across BOTH Link and ProLink — they share one redirect
    namespace (both resolve at /<code>), so codes must never collide."""
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if not Link.objects.filter(short_code=code).exists() and not ProLink.objects.filter(short_code=code).exists():
            return code


class Link(models.Model):
    original_url = models.URLField(max_length=2048)
    my_url = models.URLField(max_length=2048, blank=True, default="")
    short_code = models.CharField(max_length=16, unique=True, db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)

    @property
    def destination_url(self) -> str:
        return self.my_url or self.original_url

    def __str__(self):
        return f"{self.short_code} -> {self.destination_url}"


class ProLink(models.Model):
    """Same idea as Link, separate table — backs the new frontend only."""
    original_url = models.URLField(max_length=2048)
    my_url = models.URLField(max_length=2048, blank=True, default="")
    short_code = models.CharField(max_length=16, unique=True, db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)

    @property
    def destination_url(self) -> str:
        return self.my_url or self.original_url

    def __str__(self):
        return f"{self.short_code} -> {self.destination_url}"


class WheelRedirect(models.Model):
    """Where the Lucky Wheel's 'claim prize' button sends visitors.
    The frontend always reads the MOST RECENTLY ADDED row — add a new
    one in admin whenever you want to point the wheel somewhere else."""
    url = models.URLField(max_length=2048)
    label = models.CharField(
        max_length=100, blank=True, default="",
        help_text="Optional note for your own reference (not shown to visitors).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Wheel redirect URL"
        verbose_name_plural = "Wheel redirect URLs"

    def __str__(self):
        return f"{self.label or 'redirect'} -> {self.url} ({self.created_at:%Y-%m-%d %H:%M})"
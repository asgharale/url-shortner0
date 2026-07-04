import secrets
import string

from django.db import models

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7


def generate_short_code() -> str:
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if not Link.objects.filter(short_code=code).exists():
            return code


class Link(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=16, unique=True, db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
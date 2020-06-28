from django.db import models
from django.conf import settings

from .locators import Location


class Login(models.Model):
    ip_address = models.GenericIPAddressField()
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="logins", on_delete=models.CASCADE
    )
    reported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} in {self.city}, {self.region}, {self.country} at {self.created_at}"

    @property
    def location(self):
        return Location(self.city, self.region, self.country)

    def report(self):
        self.reported = True
        self.save()

from django.contrib import admin

from .models import Login


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "region", "country", "ip_address"]
    list_filter = ["user"]

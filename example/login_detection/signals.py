from django.contrib.auth.signals import user_logged_in

from .models import Login
from .utils import (
    get_client_ip_address,
    get_location_from_ip_address,
    detect_new_login_location,
    notify_user
)


def store_login(sender, request, user, **kwargs):
    ip_address = get_client_ip_address(request)
    location = get_location_from_ip_address(ip_address)

    if detect_new_login_location(user, location):
        notify_user(user, location, ip_address)

    Login.objects.create(
        ip_address=ip_address,
        user=user,
        city=location.city,
        region=location.region,
        country=location.country
    )


user_logged_in.connect(store_login, dispatch_uid="login_detection.store_login")

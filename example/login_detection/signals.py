from django.contrib.auth.signals import user_logged_in

from .models import Login
from .utils import (
    get_client_ip_address,
    get_location_from_ip_adress,
    detect_new_login_location
)


def store_login(sender, request, user, **kwargs):
    ip_address = get_client_ip_address(request)
    location = get_location_from_ip_adress(ip_address)

    detect_new_login_location(user, location)

    Login.objects.create(
        ip_address=ip_address,
        user=user,
        city=location.city,
        region=location.region,
        country=location.country
    )


user_logged_in.connect(store_login, dispatch_uid="login_dectection.store_login")

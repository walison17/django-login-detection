from django.contrib.auth import get_user_model

from .locators import Location, default_locator
from .models import Login

User = get_user_model()


def get_client_ip_address(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


def get_user_agent(request) -> str:
    return request.META["HTTP_USER_AGENT"]


def get_location_from_ip_address(ip_address: str) -> Location:
    return default_locator.locate(ip_address)


def detect_new_login_location(user, location: Location) -> bool:
    is_first_login = not Login.objects.filter(user=user).exists()

    if is_first_login:  # should report first login?
        return False

    last_valid_login = Login.objects.filter(user=user, reported=False).first()

    return last_valid_login.location != location


def notify_user(user: User, location: Location, ip_address: str) -> None:
    pass

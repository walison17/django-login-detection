import pytest

from django.contrib.auth import get_user_model

from ..locators import Location
from ..utils import get_client_ip_address, detect_new_login_location

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username="walison")


@pytest.fixture
def user_with_stored_login(user, store_login, location):
    store_login(user, location)
    return user


@pytest.fixture
def ip_address():
    return "158.243.15.73"


@pytest.fixture
def store_login(ip_address):
    def _store_login(user, location):
        user.logins.create(
            ip_address=ip_address,
            city=location.city,
            region=location.region,
            country=location.country,
        )

    return _store_login


@pytest.fixture
def location():
    return Location("caruaru", "pernambuco", "brazil")


def test_get_client_ip_address(rf, ip_address):
    headers = {"REMOTE_ADDR": ip_address}
    request = rf.post("/fake", **headers)

    assert get_client_ip_address(request) == ip_address


def test_get_client_ip_address_with_reverse_proxy(rf):
    headers = {"HTTP_X_FORWARDED_FOR": "177.31.176.79,127.0.0.1"}
    request = rf.post("/fake", **headers)

    assert get_client_ip_address(request) == "177.31.176.79"


@pytest.mark.django_db
def test_detect_new_login_location_first_login(user, location, mocker):
    mocked_notify_user = mocker.patch("example.login_detection.utils.notify_user")

    mocked_notify_user.assert_not_called()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "login_location,called",
    [
        (Location("caruaru", "pernambuco", "brazil"), False),
        (Location("são paulo", "são paulo", "brazil"), True),
    ],
)
def test_detect_new_login(
    user_with_stored_login, mocker, store_login, login_location, called
):
    mocked_notify_user = mocker.patch("example.login_detection.utils.notify_user")

    detect_new_login_location(user_with_stored_login, login_location)

    assert mocked_notify_user.called is called

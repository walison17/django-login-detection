import pytest

from ..locators import Location


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username="walison")


@pytest.fixture
def ip_address():
    return "158.243.15.73"


@pytest.fixture
def location():
    return Location("caruaru", "pernambuco", "brazil")

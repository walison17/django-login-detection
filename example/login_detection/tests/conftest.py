import pytest

from ..locators import Location


@pytest.fixture
def ip_address():
    return "158.243.15.73"


@pytest.fixture
def location():
    return Location("caruaru", "pernambuco", "brazil")

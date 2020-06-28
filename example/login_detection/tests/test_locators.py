import pytest
import responses

from ..locators import (
    IpLocator,
    DummyLocator,
    IpStackLocator,
    Location,
    get_locator,
)


IP_STACK_RESPONSE = {
    "ip": "177.37.000.00",
    "type": "ipv4",
    "continent_code": "SA",
    "continent_name": "South America",
    "country_code": "BR",
    "country_name": "Brazil",
    "region_code": "PE",
    "region_name": "Pernambuco",
    "city": "Caruaru",
    "zip": "55000-000",
    "latitude": -8.287919998168945,
    "longitude": -35.982749938964844,
    "location": {
        "geoname_id": 3402655,
        "capital": "Brasília",
        "languages": [{"code": "pt", "name": "Portuguese", "native": "Português"}],
        "country_flag": "http://assets.ipstack.com/flags/br.svg",
        "country_flag_emoji": "🇧🇷",
        "country_flag_emoji_unicode": "U+1F1E7 U+1F1F7",
        "calling_code": "55",
        "is_eu": False,
    },
}


@pytest.fixture
def fake_ip_locator_key():
    return "fake_ip_locator_key"


@pytest.mark.parametrize(
    "loc1,loc2,expected",
    [
        (
            Location("caruaru", "pe", "brazil"),
            Location("caruaru", "pe", "brazil"),
            True,
        ),
        (
            Location("caruaru", "pe", "brazil"),
            Location("são paulo", "sp", "brazil"),
            False,
        ),
    ],
)
def test_location__eq__(loc1, loc2, expected):
    assert (loc1 == loc2) is expected


def test_locate_must_be_implemented(ip_address):
    locator = IpLocator()

    with pytest.raises(NotImplementedError) as exc:
        locator.locate(ip_address)

    assert str(exc.value) == "locate() must be implemented."


@pytest.mark.parametrize(
    "city,region,country",
    [
        ("caruaru", "pernambuco", "brazil"),
        ("recife", "pernambuco", "brazil"),
        ("porto alegre", "rio grande do sul", "brazil"),
    ],
)
def test_dummy_locator(ip_address, city, region, country):
    locator = DummyLocator(city, region, country)

    assert locator.locate(ip_address) == Location(city, region, country)


@pytest.mark.parametrize(
    "name,options,expected",
    [
        (
            "example.login_detection.locators.DummyLocator",
            {"city": "caruaru", "region": "pe", "country": "brazil"},
            DummyLocator,
        ),
        (
            "example.login_detection.locators.IpStackLocator",
            {"api_key": "fake_ip_stack_key"},
            IpStackLocator,
        ),
    ],
)
def test_get_locator(settings, name, options, expected):
    settings.DEFAULT_IP_LOCATOR = {"NAME": name, "OPTIONS": options}

    assert isinstance(get_locator(), expected)


@responses.activate
def test_ip_stack_locator(ip_address, fake_ip_locator_key):
    responses.add(
        responses.GET,
        f"http://api.ipstack.com/{ip_address}?access_key={fake_ip_locator_key}",
        json=IP_STACK_RESPONSE
    )

    locator = IpStackLocator(api_key=fake_ip_locator_key)

    assert locator.locate(ip_address) == Location("Caruaru", "Pernambuco", "Brazil")

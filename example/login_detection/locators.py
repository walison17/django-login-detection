import requests

from django.conf import settings
from django.utils.module_loading import import_string


class Location:
    def __init__(self, city, region, country):
        self.city = city
        self.region = region
        self.country = country

    def __eq__(self, other):
        return all(
            [
                self.city == other.city,
                self.region == other.region,
                self.country == other.country,
            ]
        )


class IpLocator:
    def locate(self, ip_address) -> Location:
        raise NotImplementedError("locate() must be implemented.")


class DummyLocator(IpLocator):
    def __init__(self, city, region, country):
        self.city = city
        self.region = region
        self.country = country

    def locate(self, ip_address) -> Location:
        return Location(self.city, self.region, self.country)


class IpStackLocator(IpLocator):
    def __init__(self, api_key):
        self.api_key = api_key

    def locate(self, ip_address) -> Location:
        response = requests.get(
            f"http://api.ipstack.com/{ip_address}?access_key={self.api_key}"
        )
        data = response.json()

        return Location(
            city=data["city"], region=data["region_name"], country=data["country_name"]
        )


def get_locator() -> IpLocator:
    name, options = settings.DEFAULT_IP_LOCATOR.values()

    locator_class = import_string(name)
    return locator_class(**options)


default_locator = get_locator()

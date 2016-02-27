"""
this modules set of sample providers and service area details for each providers
"""

import random
import timeit

from django.contrib.auth.models import User
from django.contrib.gis.geos import Polygon, Point
from faker import Faker

import config
from app.models import Provider, ServiceArea


def create_providers():
    """
    creates 1000 sample provides
    :return: None
    """
    fake = Faker()
    for i in range(1000):
        provider_obj = Provider()
        provider_obj.name = fake.company()
        provider_obj.phone_number = fake.phone_number()
        provider_obj.email = "email" + str(random.randint(0, 9999)) + "@email.com"
        provider_obj.currency = config.CURRENCY[random.randint(0, len(config.CURRENCY) - 1)][0]
        provider_obj.language = config.LANGUAGES[random.randint(0, len(config.LANGUAGES) - 1)][0]
        provider_obj.created_by = User.objects.get(id=1)
        provider_obj.modified_by = User.objects.get(id=1)
        provider_obj.save()


def create_service_area():
    """
    creates service area records and associates them with random providers
    :return: None
    """
    fake = Faker()
    for i in range(1000):
        s = ServiceArea()
        s.provider = random.choice(Provider.objects.all())
        s.name = fake.word()
        s.price = fake.pyfloat(positive=True, right_digits=5, left_digits=3)
        s.area = create_random_polygon()
        s.created_by = User.objects.get(id=1)
        s.modified_by = User.objects.get(id=1)
        s.save()


def create_random_polygon():
    """
    returns to random Polygon to the call
    :return: Polygon object
    """
    latitude = random.randint(-90, 90)
    longitude = random.randint(-180, 180)
    polygons = []
    for _ in xrange(random.randint(5, 15)):
        dec_lat = random.random() / 100
        dec_lon = random.random() / 100
        point = [longitude + dec_lon, latitude + dec_lat]
        polygons.append(point)
    polygons.append(polygons[0])
    p = Polygon(polygons)
    return p


def random_points_check():
    """
    generates some random longitude and latitude, and checks the value belongs to
    any service area.
    Prints the Point and service Area object.
    :return: None
    """
    latitude = random.randint(-50, 50)
    longitude = random.randint(-180, 180)
    dec_lat = random.random() / 100
    dec_lon = random.random() / 100
    point_obj = Point(longitude + dec_lon, latitude + dec_lat)
    if ServiceArea.objects.filter(area__bbcontains=point_obj).count() > 0:
        print point_obj.json, ServiceArea.objects.filter(area__bbcontains=point_obj)


def check_time():
    """
    function to check the time taken for checking for 10000 hits
    :return: None
    """
    print timeit.Timer(random_points_check).timeit(10000)


if __name__ == "__main__":
    create_providers()
    create_service_area()
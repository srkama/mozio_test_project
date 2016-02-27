"""
models.py
ORM classes to connect with tables in databases and to perform operations.
"""

from django.db import models
from django.contrib.gis.db import models

from .model_mixins import IsActiveMixin, CreatedUpdatedMixin
import config


class Provider(IsActiveMixin, CreatedUpdatedMixin):
    """
    Provider class defines represents each provider with
    their basic information like name, contact details and
    languages
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    language = models.CharField(choices=config.LANGUAGES, max_length=5)
    currency = models.CharField(choices=config.CURRENCY, max_length=5)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class ServiceArea(IsActiveMixin, CreatedUpdatedMixin):
    """
    ServiceArea class defines each areas serviced by different provider. that
    said, one provider may have multiple service providers
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=6, max_digits=9)
    provider = models.ForeignKey(Provider)
    area = models.PolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name + " by " + self.provider.name

    @property
    def provider_name(self):
        """
        :return: provider name as a string
        """
        return self.provider.name

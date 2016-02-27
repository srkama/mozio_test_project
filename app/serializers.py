"""
serializer class for all APIs
"""

from rest_framework_gis import serializers
from rest_framework.reverse import reverse
from rest_framework import serializers as rf_serializers

from app.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    """
    Serializer for provider model
    """
    service_ares = rf_serializers.SerializerMethodField(method_name='get_service_uris')

    class Meta:
        """
        Serializer options
        """
        model = Provider
        exclude = ('created_by', 'modified_by', 'created_date', 'modified_date')
        read_only_fields = ['created_by', 'modified_by']

    def get_service_uris(self, obj):
        """
        retuns uris for provider service areas
        :param obj: provider object
        :return: uri string
        """
        return reverse('provider-service-areas', kwargs={'pk':obj.id})


class ServiceAreaSerializer(serializers.GeoModelSerializer):
    """
    Serialize for Service Area Model
    """
    provider = ProviderSerializer()

    class Meta:
        """
        Serializer options
        """
        model = ServiceArea
        exclude = ('created_by', 'modified_by', 'created_date', 'modified_date')
        read_only_fields = ['created_by', 'modified_by', 'area']


class SearchServiceAreaSerializer(serializers.GeoModelSerializer):
    """
    serializer for search results a more customized one.
    """
    provider = rf_serializers.ReadOnlyField(source='provider_name')
    provider_uri = rf_serializers.SerializerMethodField(method_name='get_provider_url')

    class Meta:
        model = ServiceArea
        exclude = ('created_by', 'modified_by', 'created_date', 'modified_date', 'area')
        read_only_fields = ['created_by', 'modified_by']

    def get_provider_url(self, obj):
        """
        method to give the respective provider URL for more details
        of provider
        :param obj: service area obj
        :return: uri string of provider detail
        """
        return reverse('provider-detail', kwargs={'pk':obj.provider.id})


class LimitedServiceAreaSerializer(serializers.GeoModelSerializer):
    """
    provides very limited detail of service
    """
    uri = rf_serializers.SerializerMethodField(method_name='get_url')

    class Meta:
        model = ServiceArea
        exclude = ('created_by', 'modified_by', 'created_date', 'modified_date', 'area', 'provider')

    def get_url(self, obj):
        """
        method to return the URI string of service area
        :param obj: service area obj
        :return uri string of service area
        """
        return reverse('services-detail', kwargs={'pk':obj.id})
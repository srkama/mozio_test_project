"""
urls routing for app
"""
from django.conf.urls import patterns, include, url
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register('provider', api.ProviderViewSet, 'provider')
router.register('service-area', api.ServiceAreaViewSet, 'services')

urlpatterns = patterns('',
                       url(r'^api/', include(router.urls)))

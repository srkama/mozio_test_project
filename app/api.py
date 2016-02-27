"""
Kamal.s
api.py

this file contains all the api endpoint definitions.

"""
import json
from rest_framework import viewsets
from rest_framework.views import Response, status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import list_route, detail_route
from django.contrib.gis.geos import Polygon, Point


from app.models import Provider, ServiceArea
from app.serializers import ServiceAreaSerializer, \
    ProviderSerializer, SearchServiceAreaSerializer, LimitedServiceAreaSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    """
    this is endpoint definition for Provider model.
    user must be authenticated to use this endpoint
    allows GET, POST, PUT and other functions as well.
    """

    model = Provider
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

    def perform_create(self, serializer):
        """
        updated create_by, modified_by based on who logged in.
        :param serializer: valid serializer obj
        """
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        """
        updated create_by, modified_by based on who logged in.
        called when object is already present
        :param serializer: valid serializer obj
        """
        serializer.save(modified_by=self.request.user)

    @detail_route()
    def service_areas(self, request, pk=None):
        """
        returns the service areas associated to the particualr provdier.
        :param pk: provider ID
        :param request: wsgi request
        :return: list of service areas as JSON object
        """
        try:
            areas = self.get_object().servicearea_set.all()
            serializer = LimitedServiceAreaSerializer(areas, many=True)
        except:
            return Response({'detail':'Some error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    service area endpoints
    user must be authenticated to use this
    allows GET, POST, PUT and other functions as well.
    """
    model = ServiceArea
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all()

    def perform_create(self, serializer):
        """
        updated create_by, modified_by based on who logged in.
        :param serializer: valid serializer obj
        """
        serializer.save(created_by=self.request.user,
                        modified_by=self.request.user,
                        area=self.get_poly_obj())

    def perform_update(self, serializer):
        """
        updated create_by, modified_by based on who logged in.
        :param serializer: valid serializer obj
        """
        serializer.save(modified_by=self.request.user,
                        area=self.get_poly_obj())

    def get_poly_obj(self):
        """
        function to convert string to Polygon object.
        if fails, raise validation error
        :return: returns the object of Polygon type
        """
        try:
            area = self.request.POST['area'].replace("\n", "")
            geo_poly_obj = Polygon(json.loads(area)['coordinates'][0])
            return geo_poly_obj
        except:
            raise ValidationError("Not proper geo json")

    @list_route(methods=['GET'])
    def find(self, request):
        """
        searches based on the given latitude and longitude
        :param request: wsgi request object
        :return: returns area and provider details
        """
        try:
            lat = float(request.GET.get('lat', ''))
            lon = float(request.GET.get('lon', ''))
        except ValueError:
            return Response({'detail': 'wrong latitude or longitude value'},
                            status.HTTP_400_BAD_REQUEST)
        point = Point(lon, lat)
        areas = ServiceArea.objects.filter(area__bbcontains=point)
        serializer = SearchServiceAreaSerializer(areas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


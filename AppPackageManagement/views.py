from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from rest_framework.exceptions import APIException
from AppPackageManagement.models import AppPkgInfo
from AppPackageManagement.serializers import AppPkgInfoSerializer, apm_package_base_path

from utils.format_tools import set_request_parameter_to_string


class AppPackagesViewSet(viewsets.ModelViewSet):

    queryset = AppPkgInfo.objects.all()
    serializer_class = AppPkgInfoSerializer

    def create(self, request, *args, **kwargs):
        """Create a resource for on-boarding an application package to a MEO"""

        set_request_parameter_to_string(request, 'userDefinedData')
        request.data['_links'] = {
            'self': request.build_absolute_uri(),
            'appD': request.build_absolute_uri(),
            'appPkgContent': request.build_absolute_uri()
        }
        return super().create(request)

    # def get_success_headers(self, data):
    #     return {'Location': data['_links']['self']}

    def list(self, request, *args, **kwargs):
        """Queries information relating to on-boarded application packages in the MEO.
            The GET method queries the information of the App packages matching the filter
        """
        if self.get_queryset().__len__() < 1:
            raise APIException(
                detail=
                'One or more individual App Package resource have not been created',
                code=status.HTTP_409_CONFLICT)

        return super().list(request)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

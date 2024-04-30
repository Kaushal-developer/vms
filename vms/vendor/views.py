from django.shortcuts import render

# Create your views here.
from rest_framework import permissions,status
from lib import constants
from lib import permissions as custom_permission
from lib.views import BaseViewSet
from . import models
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response



class VendorViewSet(BaseViewSet):
    model = models.Vendor
    permission_classes=[ permissions.IsAuthenticated & custom_permission.customReadWritePermission]
    view_serializers = {
        constants.Action.LIST: serializers.VendorListSerializer,
        constants.Action.RETRIEVE: serializers.VendorSerializer,
        constants.Action.VIEW: serializers.VendorDetailSerializer,
    }

    @action(methods=[constants.Method.GET], detail=True)
    def performance(self,request, *args, **kwargs):
        vendor = self.get_object()
        performace_obj = vendor.vendor_performance.all()
        performance_ser = serializers.HistoricalPerformanceListSerializer(performace_obj,many=True).data
        return Response(data={'data': performance_ser,'message':'List of performance metrics data'},
                        status=status.HTTP_200_OK)  

# class VendorHistoricalPerformanceViewSet(BaseViewSet):
#     model = models.HistoricalPerformanceModel
#     permission_classes=[ permissions.IsAuthenticated & custom_permission.customReadWritePermission]
#     view_serializers = {
#         constants.Action.LIST: serializers.HistoricalPerformanceListSerializer,
#         constants.Action.RETRIEVE: serializers.HistoricalPerformanceSerialzier,
#         constants.Action.VIEW: serializers.HistoricalPerformanceDetailSerializer,
#     }
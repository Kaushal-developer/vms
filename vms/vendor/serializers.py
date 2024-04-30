import logging
from rest_framework import serializers
from lib import constants
from lib.serializers import DynamicFieldsModelSerializer, ReadOnlyModelSerializer
from . import models

logger = logging.getLogger(__name__)

"""
Vendor Serializers
"""

class VendorListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ("id", "name","contact_details","address","vendor_code","on_time_delivery_rate","quality_rating_avg","average_response_time","fulfillment_rate")


class VendorDetailSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = models.Vendor
        fields = ("id", "name", "contact_details", "address","vendor_code","on_time_delivery_rate","quality_rating_avg","average_response_time","fulfillment_rate")


class VendorSerializer(DynamicFieldsModelSerializer):
    name = serializers.CharField(max_length=255)
    class Meta:
        model = models.Vendor
        fields = ("id", "name", "contact_details", "address","vendor_code","on_time_delivery_rate","quality_rating_avg","average_response_time","fulfillment_rate",'response_message')

    def validate_name(self, value):
        error_message = "Vendor with provided name already exists."
        return self.unique_value_validator(
            field="name", value=value, error_message=error_message,look_up="name__iexact"
        )

    def validate_contact_details(self, value):
        error_message = "Vendor with provided contact number already exists."
        return self.unique_value_validator(field="contact_details", value=value, error_message=error_message, look_up="contact_details__iexact")
    

"""
Vendor Historical Performance Serializers
"""

class HistoricalPerformanceListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = models.HistoricalPerformanceModel
        fields = ("id", "vendor","record_date","on_time_delivery_rate", "quality_rating_avg","average_response_time","fulfillment_rate",)


class HistoricalPerformanceDetailSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = models.HistoricalPerformanceModel
        fields = ("id", "vendor","record_date","on_time_delivery_rate", "quality_rating_avg","average_response_time","fulfillment_rate",)


class HistoricalPerformanceSerialzier(DynamicFieldsModelSerializer):
    class Meta:
        model = models.HistoricalPerformanceModel   
        fields = ("id", "vendor","record_date","on_time_delivery_rate", "quality_rating_avg","average_response_time","fulfillment_rate",)

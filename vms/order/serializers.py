import logging
from lib.serializers import DynamicFieldsModelSerializer, ReadOnlyModelSerializer
from . import models
logger = logging.getLogger(__name__)

"""
Order Serializers
"""

class PurchaseOrderDetailSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = models.PurchaseOrder
        fields = ("id", "po_number", "vendor", "order_date", "delivery_date","items","quantity","status","quality_rating","issue_date",'acknowledgment_date')


class PurchaseOrderListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = models.PurchaseOrder
        fields = ("id", "po_number", "vendor", "order_date", "delivery_date","items","quantity","status","quality_rating","issue_date",'acknowledgment_date')


class PurchaseOrderSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = models.PurchaseOrder
        fields = ("id", "po_number", "vendor", "order_date", "delivery_date","items","quantity","status","quality_rating","issue_date",'acknowledgment_date','response_message')

    
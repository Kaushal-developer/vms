from rest_framework import permissions,status
from lib import constants
from lib import permissions as custom_permission
from lib.views import BaseViewSet
from . import models
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response


class PurchaseOrderViewSet(BaseViewSet):
    model = models.PurchaseOrder
    permission_classes = [
        permissions.IsAuthenticated & custom_permission.customReadWritePermission 
    ]
    view_serializers = {
        constants.Action.LIST: serializers.PurchaseOrderListSerializer,
        constants.Action.RETRIEVE: serializers.PurchaseOrderSerializer,
        constants.Action.VIEW: serializers.PurchaseOrderDetailSerializer,
    }

    @action(methods=[constants.Method.POST], detail=True)
    def acknowledge(self,request, *args, **kwargs):
        p_order = self.get_object()
        data =request.data
        if 'acknowledgment_date' not in data:
            return Response(data={'message':'Acknowledgment Date should not be None'},
                        status=status.HTTP_200_OK)  
        po_ser = serializers.PurchaseOrderSerializer(p_order,data=data,partial=True)
        if po_ser.is_valid():
            po_ser.save()
        return Response(data={'data': po_ser.data,'message':po_ser.data['response_message']},
                        status=status.HTTP_200_OK)  

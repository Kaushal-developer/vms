from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from lib.models import BaseModel
from vendor import models as vendor_models
from lib import constants
import random,string
from django_lifecycle import AFTER_UPDATE, hook
from django.db.models import Avg, F,ExpressionWrapper, fields

from django_lifecycle.conditions import WhenFieldHasChanged

class PurchaseOrder(BaseModel):
    po_number = models.CharField(_('PO Number'), max_length=150,null=True,blank=True)
    vendor = models.ForeignKey(vendor_models.Vendor, on_delete=models.CASCADE, verbose_name='Vendor',related_name='vendor_order')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField(_('Items'))
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=255,choices=constants.OrderConstants.get_order_status_choices(),default=constants.OrderConstants.PENDING)
    quality_rating = models.FloatField(default=0)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)


    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Purchase Order"
        ordering = BaseModel.ORDERING

    @property
    def response_message(self) -> str:
        model_name = self.__class__._meta.verbose_name.title()
        response_message = f"{model_name} - {self.po_number}"
        return response_message
    
    def __str__(self) -> str:
        return f"{self.po_number}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created (not updated)
            # Generate a unique PO number
            self.po_number = self.generate_po_number()
        super().save(*args, **kwargs)

    def generate_po_number(self):
        po = PurchaseOrder.objects.last()
        acronym = "".join((random.choice(string.ascii_uppercase) for x in range(4)))
        if po:
            po_num = 'PO%010d' % (int(po.id)+1)
        else:
            po_num = 'PO%010d' % (1)    
        po_id = po_num + acronym
        return po_id

    @hook(AFTER_UPDATE, when="status", was=constants.OrderConstants.PENDING, is_now=constants.OrderConstants.COMPLETED)
    def on_status_change(self):
        '''
        calculate on time delivery Rate
        '''
        on_time_delivery_rate = 0
        average_quality_rating = 0
        vendor = self.vendor
        completed_pos_count = PurchaseOrder.objects.filter(
            vendor_id=self.vendor.id,
            status=constants.OrderConstants.COMPLETED,
            delivery_date__lte=self.delivery_date
        ).count()
        total_completed_pos_count = PurchaseOrder.objects.filter(
            vendor=vendor,
            status=constants.OrderConstants.COMPLETED
        ).count()
        if total_completed_pos_count > 0:
            on_time_delivery_rate = completed_pos_count / total_completed_pos_count

        '''
        Quality Rating Average:
        '''
        average_quality_rating_query = PurchaseOrder.objects.filter(
            vendor=vendor,
            status=constants.OrderConstants.COMPLETED
        ).aggregate(
            average_quality_rating=Avg('quality_rating')
        )
        average_quality_rating = average_quality_rating_query['average_quality_rating']
        
        vendor.average_quality_rating = average_quality_rating if average_quality_rating else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

    '''Average Response Time'''
    @hook(AFTER_UPDATE, condition=WhenFieldHasChanged("acknowledgment_date", has_changed=True))
    def update_review(self):
        time_difference_expression = ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=fields.DurationField()
            )
        average_time_difference = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            acknowledgment_date__isnull=False, 
        ).aggregate(
            average_time_difference=Avg(time_difference_expression)
        )
        average_time_difference_days = average_time_difference['average_time_difference'].days
        if average_time_difference:
            vendor = self.vendor
            vendor.average_response_time = abs(average_time_difference_days) # converted in terms of days
            vendor.save()

    @hook(AFTER_UPDATE, condition=WhenFieldHasChanged("status", has_changed=True))
    def update_fulfilment_ratio(self):
        fulfillment_ratio = 0
        fulfilled_pos_count = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status=constants.OrderConstants.COMPLETED,
        ).count()
        total_pos_count = PurchaseOrder.objects.filter(vendor=self.vendor).count()
        if total_pos_count > 0:
            fulfillment_ratio = fulfilled_pos_count / total_pos_count
        else:
            fulfillment_ratio = 0
        if fulfillment_ratio:
            vendor = self.vendor
            vendor.fulfillment_rate = fulfillment_ratio
            vendor.save()


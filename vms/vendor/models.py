from django.db import models
from django.utils.translation import gettext_lazy as _
from lib.models import BaseModel
from vendor import models as vendor_models
from lib import helpers
from django_lifecycle import AFTER_UPDATE, hook
from django_lifecycle.conditions import WhenFieldHasChanged


class Vendor(BaseModel):
    name = models.CharField(_('Vendor Name'), max_length=150, unique=True)
    address = models.CharField(_('Vendor Address'), max_length=255, null=True, blank=True)
    contact_details = models.TextField(_('Vendor Contact Details'))    
    vendor_code = models.CharField(_('Vendor Code'), max_length=150, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate=models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Vendors"
        verbose_name = "Vendor"
        ordering = BaseModel.ORDERING

    @property
    def response_message(self) -> str:
        model_name = self.__class__._meta.verbose_name.title()
        response_message = f"{model_name} - {self.name}"
        return response_message
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    @hook(AFTER_UPDATE, condition=WhenFieldHasChanged("on_time_delivery_rate", has_changed=True))
    @hook(AFTER_UPDATE, condition=WhenFieldHasChanged("quality_rating_avg", has_changed=True))
    @hook(AFTER_UPDATE, condition=WhenFieldHasChanged("average_response_time", has_changed=True))
    @hook(AFTER_UPDATE, condition=WhenFieldHasChanged("fulfillment_rate", has_changed=True))
    def handle_update(self):
        HistoricalPerformanceModel.objects.create(vendor=self,on_time_delivery_rate=self.on_time_delivery_rate,quality_rating_avg=self.quality_rating_avg,average_response_time=self.average_response_time,fulfillment_rate=self.fulfillment_rate)
        print(1212121,'created')
        
class HistoricalPerformanceModel(BaseModel):
    vendor = models.ForeignKey(vendor_models.Vendor, on_delete=models.CASCADE, verbose_name='Vendor',related_name='vendor_performance')
    record_date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Performance Model"
        verbose_name = "Performance Model"
        ordering = BaseModel.ORDERING

    @property
    def response_message(self) -> str:
        model_name = self.__class__._meta.verbose_name.title()
        response_message = f"{model_name} - {self.name}"
        return response_message
    
    def __str__(self) -> str:
        return f"{self.vendor}-{helpers.format_date_time(self.date)}"

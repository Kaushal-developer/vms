from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views
app_label = 'order'

order_router = DefaultRouter()
order_router.register('orders', views.PurchaseOrderViewSet, basename='purchase_order')

urlpatterns = [
    path('', include(order_router.urls)),
]

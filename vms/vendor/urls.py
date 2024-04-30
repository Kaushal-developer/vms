from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views
app_label = 'vendor'

vendor_router = DefaultRouter()
vendor_router.register('vendors', views.VendorViewSet, basename='vendor')

urlpatterns = [
    path('', include(vendor_router.urls)),
]

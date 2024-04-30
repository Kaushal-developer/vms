from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(("order.urls", "order"), namespace="order")),  # For order module
    path("api/", include(("vendor.urls", "vendor"), namespace="vendor")), 
    path('generate_token/', auth_views.LoginView.as_view(), name='login'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog import views

from customers.views import view_lk

urlpatterns = [
    # path('', index),
    path('admin/', admin.site.urls),
    path('lk/', view_lk, name='lk'),
    path('accounts/', include('customers.urls')),  # /accounts/signup, /accounts/login
    path('', views.index)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

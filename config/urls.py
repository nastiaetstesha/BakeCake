from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog import views
from orders import views as order_views

from customers.views import view_lk

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lk/', view_lk, name='lk'),
    path('accounts/', include('customers.urls')),  # /accounts/signup, /accounts/login
    path('', views.index),
    path('orders/create/', order_views.create, name='order_create'),
    path('orders/price/',  order_views.price,  name='order_price'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

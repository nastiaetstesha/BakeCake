from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# from customers import views
from customers.views import ClientProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lk/', ClientProfileView.as_view(), name='lk'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
